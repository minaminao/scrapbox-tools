# scrapbox-tools

### 孤立ページを見つける
リンクするページもリンクされるページも無い。
`A -> 存在しないページ <- B`の場合はA,Bは孤立ページと見なさない。

```sh
python find_lonely_page.py foo.json
```

### 最初に作られたページタイトルと日時を出力する

```sh
python find_first_page.py foo.json
```

