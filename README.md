# jphrase
jphraseは、日本語のテキストを文節に分割するためのライブラリです。
形態素解析から得られた単語の品詞情報に基づき、ルールベースで文節を決定します。

# Basic Usage

```Python
from jphrase import PhraseSplitter
splitter = PhraseSplitter()
print(splitter.split_text("今日はよく寝ました"))
```

```
['今日は', 'よく', '寝ました']
```

```Python
splitter = PhraseSplitter(output_type = PhraseSplitter.OUTPUT_DETAILED)
phrases = splitter.split_text("今日はよく寝ました")
for phrase in phrases:
  print(phrase)
```

```
[{'surface_form': '今日', 'pos': '名詞', 'pos_detail_1': '副詞可能', 'pos_detail_2': '*', 'pos_detail_3': '*', 'conjugated_type': '*', 'conjugated_form': '*', 'basic_form': '今日', 'reading': 'キョウ', 'pronunciation': 'キョー'}, {'surface_form': 'は', 'pos': '助詞', 'pos_detail_1': '係助詞', 'pos_detail_2': '*', 'pos_detail_3': '*', 'conjugated_type': '*', 'conjugated_form': '*', 'basic_form': 'は', 'reading': 'ハ', 'pronunciation': 'ワ'}]
[{'surface_form': 'よく', 'pos': '副詞', 'pos_detail_1': '一般', 'pos_detail_2': '*', 'pos_detail_3': '*', 'conjugated_type': '*', 'conjugated_form': '*', 'basic_form': 'よく', 'reading': 'ヨク', 'pronunciation': 'ヨク'}]
[{'surface_form': '寝', 'pos': '動詞', 'pos_detail_1': '自立', 'pos_detail_2': '*', 'pos_detail_3': '*', 'conjugated_type': '一段', 'conjugated_form': '連用形', 'basic_form': '寝る', 'reading': 'ネ', 'pronunciation': 'ネ'}, {'surface_form': 'まし', 'pos': '助動詞', 'pos_detail_1': '*', 'pos_detail_2': '*', 'pos_detail_3': '*', 'conjugated_type': '特殊・マス', 'conjugated_form': '連用形', 'basic_form': 'ます', 'reading': 'マシ', 'pronunciation': 'マシ'}, {'surface_form': 'た', 'pos': '助動詞', 'pos_detail_1': '*', 'pos_detail_2': '*', 'pos_detail_3': '*', 'conjugated_type': '特殊・タ', 'conjugated_form': '基本形', 'basic_form': 'た', 'reading': 'タ', 'pronunciation': 'タ'}]
```

# Installation

```
pip install jphrase
```

形態素解析ライブラリと辞書もインストールしてください。

```
pip install mecab-python3 ipadic
```

mecab-python3以外の形態素解析ライブラリ、ipadic以外の辞書には現状非対応です。

# Usage

PhraseSplitterのインスタンスを作成し、split_textメソッドで分割を実行してください。

```Python
from jphrase import PhraseSplitter
splitter = PhraseSplitter()
input_string = "今日はよく寝ていました"
phrases = splitter.split_text(input_string)
```

split_textにオプション引数を渡すことで、出力形式を調整できます。

```Python
phrases = splitter.split_text(input_string, output_type = PhraseSplitter.OUTPUT_SURFACE, consider_non_independent_nouns_and_verbs_as_breaks = True)
```

output_type引数は、PhraseSplitterクラスのsplit_textメソッドの出力形式を指定するために使用されます。利用可能な出力形式は以下の通りです:

1. `PhraseSplitter.OUTPUT_SURFACE`: 分割されたテキストを表層形のみで返します。各フレーズは文字列のリストとして返されます。
2. `PhraseSplitter.OUTPUT_DETAILED`: 分割されたテキストを詳細な形態素情報と共に返します。各フレーズは辞書のリストとして返され、各辞書には形態素の表層形、品詞、読み、発音などの情報が含まれます。
3. `PhraseSplitter.OUTPUT_CONCATENATED`: 分割されたテキストを連結された形で返します。各フレーズは表層形、読み、発音を含む辞書として返されます。

output_type引数を指定しない場合、デフォルトの出力形式は`PhraseSplitter.OUTPUT_SURFACE`です。

consider_non_independent_nouns_and_verbs_as_breaks引数は、非自立な名詞や動詞を文節の区切りとして扱うかどうかを制御します。この引数がTrueに設定されている場合、非自立な名詞や動詞の前で新しい文節が始まります。Falseの場合、非自立な名詞や動詞は前の文節に含まれ続けます。

またこれらのオプション引数はPhraseSplitterのインスタンス作成時にも指定することができ、指定した場合は、split_text実行時のデフォルト値として扱われます。

# Testing

```Python
python tests/test_phrase_splitter.py
```

# Rule for phrase splitting
jphraseでは形態素解析結果の品詞情報に基づいて文節の境界を決定します。

ipadicの辞書を用いて形態素解析を行うと、各単語につき、以下の情報が得られます。

```
表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
```

基本的には品詞が「名詞」「動詞」「副詞」「感動詞」「形容詞」「形容動詞」「連体詞」「接頭詞」のとき、その単語の直前を文節の境界とみなします。
ただし以下の条件に該当する場合は文節の境界とはみなさないようにします。

|種類|例|判断方法|
|---|---|---|
|接尾辞|「痛さ」の「さ」など|品詞が「名詞」かつ品詞細分類に「接尾」が含まれている|
|接頭詞の直後の単語|「お美しい」の「美しい」など（「お」が接頭詞）|直前の単語の品詞が「接頭詞」である|
|サ変接続名詞の直後のサ変接続動詞|「勉強する」の「する」など|品詞が「動詞」、かつ、活用型が「サ変・スル」、かつ、直前の単語の品詞細分類に「サ変接続」が含まれている（注１）|
|非自立な名詞（注２）|動詞や形容詞などの直後の「もの」「こと」や、「やったのか？」の「もの・こと」という意味の「の」など|品詞が「名詞」かつ品詞細分類に「非自立」が含まれている|
|非自立な動詞（注２）|「やっている」の「いる」など|品詞が「動詞」かつ品詞細分類に「非自立」が含まれている|

注１：辞書によっては、記号が「サ変接続」になって、その周辺の処理の精度が悪くなることがあるので注意。

注２：jphraseではオプションによって非自立な名詞，動詞を文節の境界とするかどうか選択可能。これらは文法的には文節の境界とするのが正しいが、実際に結果を眺めた際に、分割が細かすぎると感じられるケースもあったため、そのようにした。

また上記以外に、主に記号と連続するケースなどにおいて、より細かな例外処理が存在します。詳細はソースコードを参照してください。

# Licensing

jphraseはMITライセンスの下で公開されています。
ただし、jphraseを使用する際に必要となる追加のライブラリや辞書は、それぞれのライセンス条項に従ってください。

