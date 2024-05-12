
class PhraseSplitter:
    OUTPUT_SURFACE = 'surface'
    OUTPUT_DETAILED = 'detailed'
    OUTPUT_CONCATENATED = 'concatenated'

    def __init__(self
                 , output_type=OUTPUT_SURFACE
                 , consider_non_independent_nouns_and_verbs_as_breaks=True):
        import MeCab, ipadic
        self.__tokenize = self.create_tokenizer_from_mecab_ipadic(MeCab.Tagger(ipadic.MECAB_ARGS))
        self.output_type = output_type
        self.consider_non_independent_nouns_and_verbs_as_breaks = consider_non_independent_nouns_and_verbs_as_breaks
    
    def create_tokenizer_from_mecab_ipadic(self, tagger) -> callable:
        
        def tokenize(text: str) -> list[dict]:
            mecab_result = tagger.parse(text).splitlines()
            mecab_result = mecab_result[:-1]  # Remove the last line as it is unnecessary
            tokens = []
            for line in mecab_result:
                if '\t' not in line:
                    continue
                parts = line.split('\t')
                word_surface = parts[0]  # Surface form of the word
                pos_info = parts[1].split(',')  # Part of speech and other grammatical information
                token = {
                    'surface_form': word_surface,
                    'pos': pos_info[0],
                    'pos_detail_1': pos_info[1] if len(pos_info) > 1 else '*',
                    'pos_detail_2': pos_info[2] if len(pos_info) > 2 else '*',
                    'pos_detail_3': pos_info[3] if len(pos_info) > 3 else '*',
                    'conjugated_type': pos_info[4] if len(pos_info) > 4 else '*',
                    'conjugated_form': pos_info[5] if len(pos_info) > 5 else '*',
                    'basic_form': pos_info[6] if len(pos_info) > 6 else word_surface,
                    'reading': pos_info[7] if len(pos_info) > 7 else '',
                    'pronunciation': pos_info[8] if len(pos_info) > 8 else ''
                }
                tokens.append(token)
            return tokens
        
        return tokenize

    # This method is intended to be replaced by the tokenizer defined in __init__, so it is left empty here.
    def __tokenize(self, text: str) -> list[dict]:
        pass
    
    def __should_break_before_token(self, token: dict, current_phrase: list[dict], consider_non_independent_nouns_and_verbs_as_breaks: bool = True) -> bool:

        if not current_phrase:
            return False
        if all(_token['pos'] == '記号' for _token in current_phrase):
            return False
                    
        phrase_break_pos_tags = ['名詞', '動詞', '接頭詞', '副詞', '感動詞', '形容詞', '形容動詞', '連体詞']
        open_bra = '「『（【｛〈《〘〚)]}'
        close_bra = '」』）】｝〉》〙〗)]}'
        
        pos_info = token['pos']
        pos_detail = ','.join([token['pos_detail_1'], token['pos_detail_2'], token['pos_detail_3']])

        previous_token = current_phrase[-1]
        previous_pos_info = previous_token['pos']
        previous_pos_detail = ','.join([previous_token['pos_detail_1'], previous_token['pos_detail_2'], previous_token['pos_detail_3']])


        if pos_info == '記号' and token['surface_form'] not in open_bra:
            return False
        
        is_phrase_break_pos = pos_info in phrase_break_pos_tags or token['surface_form'] in open_bra
        if not consider_non_independent_nouns_and_verbs_as_breaks and '非自立' in pos_detail:
            is_phrase_break_pos = False

        if is_phrase_break_pos:
            if previous_pos_info == '接頭詞' or previous_token['surface_form'] in open_bra:
                return False
            elif '接尾' in pos_detail:
                return False
            elif token['conjugated_type'] == 'サ変・スル' and 'サ変接続' in previous_pos_detail:
                return False
                        
            return True
        else:
            if previous_pos_info == '記号' and previous_token['surface_form'] not in close_bra:
                return True
            
            return False
                
        return True
            
        
    def __split_text_into_detailed_phrases(self, text: str, consider_non_independent_nouns_and_verbs_as_breaks: bool = True) -> list[list[dict]]:
        tokens = self.__tokenize(text)
        segmented_text = []
        current_phrase = []

        for token in tokens:
            should_break = self.__should_break_before_token(token, current_phrase, consider_non_independent_nouns_and_verbs_as_breaks)
            if should_break:
                if current_phrase:
                    segmented_text.append(current_phrase)
                current_phrase = []
            current_phrase.append(token)

        if current_phrase:
            segmented_text.append(current_phrase)
        return segmented_text
    
    def __split_text_into_surface_phrases(self, text: str, consider_non_independent_nouns_and_verbs_as_breaks: bool = True) -> list[str]:
        detailed_phrases = self.__split_text_into_detailed_phrases(text, consider_non_independent_nouns_and_verbs_as_breaks)
        surface_phrases = [''.join(token['surface_form'] for token in phrase) for phrase in detailed_phrases]
        return surface_phrases
    
    def __split_text_into_concatenated_phrases(self, text: str, consider_non_independent_nouns_and_verbs_as_breaks: bool = True) -> list[dict]:
        detailed_phrases = self.__split_text_into_detailed_phrases(text, consider_non_independent_nouns_and_verbs_as_breaks)
        concatenated_phrases = []
        for phrase in detailed_phrases:
            concatenated_phrase = {
                'surface_form': ''.join(token['surface_form'] for token in phrase),
                'pronunciation': ''.join(token['pronunciation'] for token in phrase if token['pronunciation'] and token['pos'] != '記号'),
                'reading': ''.join(token['reading'] for token in phrase if token['reading'] and token['pos'] != '記号')
            }
            concatenated_phrases.append(concatenated_phrase)
        return concatenated_phrases
    def split_text(self, text: str, output_type: str = None, consider_non_independent_nouns_and_verbs_as_breaks: bool = None):
        if consider_non_independent_nouns_and_verbs_as_breaks is None:
            consider_non_independent_nouns_and_verbs_as_breaks = self.consider_non_independent_nouns_and_verbs_as_breaks
        output_type = output_type or self.output_type
        split_methods = {
            self.OUTPUT_SURFACE: self.__split_text_into_surface_phrases,
            self.OUTPUT_DETAILED: self.__split_text_into_detailed_phrases,
            self.OUTPUT_CONCATENATED: self.__split_text_into_concatenated_phrases
        }
        if output_type in split_methods:
            return split_methods[output_type](text, consider_non_independent_nouns_and_verbs_as_breaks)
        else:
            valid_types = ', '.join(split_methods.keys())
            raise ValueError(f"Invalid output type specified. Choose {valid_types}.")
        
if __name__=='__main__':
    print(PhraseSplitter().split_text('「て。」や「に」などの'))