from setuptools import setup, find_packages

setup(
    name="jphrase",  # PyPIに登録するパッケージ名
    version="0.0.2",
    packages=find_packages(where='src'),  # パッケージはsrcディレクトリ内にある
    package_dir={'': 'src'},  # パッケージのルートディレクトリをsrcに設定
    install_requires=[],
    author="shimajiroxyz",
    author_email="shimajiroxyz@users.noreply.github.com",
    description="A Japanese phrase tokenizer",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/jiroshimaya/jphrase",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
