# 使い方
1. [足す小説]と[引く小説]それぞれに小説の題名を記入する。
    * 片方の欄が空白のままでも大丈夫。
    * 複数ある場合は、全角または半角スペースで区切る。
2. [計算]ボタンを押す。
3. 1.での計算の結果に似ている順に小説が表示される。
    * 表右側に表示される数値は**類似度**。

#### 例
* 足す小説 : `こころ 銀河鉄道の夜`
* 引く小説 : `星の王子さま`

こう書くと、『こころ』+『銀河鉄道の夜』-『星の王子さま』という **小説の計算** が行われる。

#### 活用例
* 好きな小説を5冊挙げ、全て[足す小説]に書く。→次に読むべき1冊が見つかるかも？？

# Novel2Vecについて
#### Novel2Vecとは、小説とそのベクトル表現を対応付けるモデルである
ベクトルは各種演算ができるため、このモデルによって

* 小説を足し算、引き算する
* 任意のベクトルと方向が似ている小説を求める

ことができる。また、ベクトルには方向があるため、この方向が何かしらの**有意な成分**を示していると考えられている。

何かをベクトル表現するというアイデアは**単語**にもある(Word2Vecという)。こちらは

* `王`-`男`+`女`=`女王`
* `お兄さん`-`おじさん`=`優しい`

などの計算ができることが知られている[2]。

#### Novel2Vecが作られるまで
Novel2Vecでは、Word2Vecのアイデアを小説に流用している。実際、Novel2VecはWord2Vecのモデルを作成するライブラリ`gensim.models.Word2Vec`を使用して作成されている。

Word2Vecは、文章を機械に沢山読ませることで作られた。

これにならい、Novel2Vecは、2018～2020/10/25にTwitter上に投稿された[1]`#名刺代わりの小説10選`というハッシュタグを持つツイート約8,000件(https://github.com/GINK03/novel_recommend/blob/master/var/shosetsu_dataset.csv) から小説の題名を抽出し、それらを機械に読ませて作った。

#### 現行のNovel2Vecモデルの詳細
> 学習アルゴリズム : `Skip-gram`
> Gensimバージョン : `4`
> ベクトル次元数 : `100`

#### 参考
1. GINK03 .(2020). novel recommended. https://gink03.github.io/novel_recommend/. 2021/08/17アクセス
2. パソコン工房NEXMAG. (2018). Word2Vecで「おじさん」と「お兄さん」を比較してみた. https://www.pc-koubou.jp/magazine/9905. 2021/08/17アクセス

# 注意
* 入力欄には個人情報を書き込まないこと。
* 小説の引き算という計算が何を意味しているのか、Mya-Myaはよく分かっていない。
* 小説の題名を抽出する処理において、小説の題名ではないノイズデータがいくつか混ざってしまった。このため、計算結果に小説の題名ではない文字列が表示されることがある。
