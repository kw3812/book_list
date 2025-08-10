// jsonデータを読み込み
const book_list = async () => {
  const res = await fetch('./book.json');
  const json = await res.json();
  return json;
}
// jsonデータをhtmlに出力
// pram search_title[str, bool], sort(str)
// return none
let view_list = async (search_title,sort) => {
    // jsonデータ読み込みの関数(const不可)
    let books = await book_list();
    const list_id = document.getElementById("list_id");

    // IDの降順でソート
    books.sort((a, b) => b[0] - a[0]);       

    // books[5] の昇順でソート（所蔵 ＞ 廃棄） 
    books.sort((a, b) => a[5].localeCompare(b[5]));

    // 検索ワードを含むで抽出（配列が空でない場合）
  if (search_title[0]) {
    // タイトルで検索
    if (search_title[1] == true) {
      books = books.filter(function (value) {
        return value[1].includes(search_title[0]);
      })
    } // 著者で検索
    else {
      books = books.filter(function (value) {
        return value[2].includes(search_title[0]);
      })
    }
  }
  // 並び替え
  // 著者名のカナ降順
  if (sort == "rubi_desc") {
    books.sort(function (a, b) {
      return (a[3] > b[3]) ? -1 : 1;
    })
  }
  // 著者名のカナ昇順
  else if (sort == "rubi_asc") {
    books.sort(function (a, b) {
      return (a[3] < b[3]) ? -1 : 1;
    });
  }

    // モーダルを表示して詳細情報を表示
  function book_detail(book) {
    const modal = document.getElementById('book_modal');
    const modal_title = document.getElementById('title');
    const modal_writer = document.getElementById('writer');
    const modal_publisher = document.getElementById('publisher');
    const modal_disp = document.getElementById('memo');
    modal_title.textContent = `タイトル: ${book[1]}`;
    modal_writer.textContent = `著者: ${book[2]}`;
    modal_publisher.textContent = `出版社: ${book[4]}`;
    modal_disp.textContent = `内容: ${book[7]}`;
  
    modal.style.display = 'block'; // モーダルを表示
  }
  // モーダルを閉じる処理
    const modal_close = document.getElementById('modal_close');
    modal_close.addEventListener('click', function () {
      const modal = document.getElementById('book_modal');
      modal.style.display = 'none';
});
    // ループ処理　（リスト表示）
    for (let i = 0; i < books.length; i++) {
      const list_li = document.createElement('li');

      title = `<span class="li_title">${books[i][1]}</span>` 
      writer = `<span class="li_writer">${books[i][2]}</span>` 
      publisher = `<span class="li_publisher">${books[i][4]}</span>` 
      disp = `<span class="li_disp">${books[i][5]}</span>` 
      // タイトル・著者名・出版社・所蔵（◯ or ☓）
      textContent =`${title}${writer}${publisher}${disp}`
      list_li.innerHTML  = (textContent);
      
      // クリックイベントを追加して詳細画面に移動
      list_li.addEventListener('click', function () {
        book_detail(books[i]); // 詳細表示関数を呼び出す
      });

      list_id.appendChild(list_li);
    }

    // 件数表示
    const data_count = document.getElementById("data_count");
    count = books.length
    data_count.textContent=`${count}件`
}

// データリストの削除
let restate = () =>{
  // 子要素を全て削除
  while (list_id.firstChild) {
    list_id.removeChild(list_id.firstChild);
  }
}

//  クリア・初期化
function cls(){
  restate()
  // 並び替え初期
  sort_id = document.getElementById("sort");
  sort_id.options[0].selected = true;
  // ラジオボタン初期
  document.search_form.radio_btn[0].checked =true;
  search_title_id = document.getElementById("title_search");
  // 検索ワードクリア
  search_title_id.value = '';
  search_title = []
  sort = ''
  view_list(search_title, sort)
}

