
// fetch html
use reqwest;
use scraper::{Html, Selector};
use std::error::Error;
use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::Path;

struct ComicInfo {
    title: String,
    link: String,
    id: String,
}

use std::thread;
use std::time::Duration;

use indicatif::{ProgressBar, ProgressStyle};

// get comic information with a keyword(like 'boudica') and a page number
fn load_info(keyword: String, page: u64) {
    // generate a new addr with provided  keyword and page number
    let mut addr: String = String::from("https://nyahentai.biz/page/");
    addr = addr + &page.to_string() + &String::from("?s=") + &keyword;
    println!("load addr {}", addr);
    //let addr: String = String::from("https://nyahentai.biz/page/1?s=boudica"); // search with keyword "boudica" on page 1
    let resp = reqwest::blocking::get(addr).expect("bad request");
    let content = resp.text().unwrap();
    // html source code has been saved in source.html
    //let path = Path::new("/home/lagrange/Desktop/NJU/learn_rust/source.html");
    /*
    let path = Path::new("D:\\NJU\\get_comic\\source.html");
    let mut file = File::create(&path).unwrap();
    file.write(content.as_bytes()).unwrap();
    */
    // select <article section and get id, title, addr
    let article_selector = Selector::parse("article").unwrap();
    let document = Html::parse_document(&content);
    let all_article = document.select(&article_selector);

    println!("keyword: {}", keyword);
    println!("page: {}", page);

    let mut file = OpenOptions::new()
        .append(true)
        //.open("/home/lagrange/Desktop/NJU/learn_rust/comic_set.yaml")
        .open("D:\\NJU\\get_comic\\comic_set.yaml")
        .expect("giao!");
    
    // get each comic info
    // add a progress bar
    let spinner_style = ProgressStyle::default_spinner().tick_chars("⠁⠂⠄⡀⢀⠠⠐⠈ ");
    let pb = ProgressBar::new_spinner(); // 使用自旋进度条，如果能获取Select类型的all_article的长度，则使用正常的条状进度条
    pb.set_style(spinner_style);
    for article in all_article {
        let mut comic_info = ComicInfo {
            // initialize comic information formation, if following action does not go well, comic_set.yaml will show 'Bad info' series
            title: String::from("Bad title"),
            link: String::from("Bad link"),
            id: String::from("Bad id"),
        };
        let id = article.value().attr("id"); // id here might be null, Some() is an optional type
        if let Some(post_id) = id {
            //println!("{post_id}");
            comic_info.id = String::from(post_id);
        } else {
            println!("Empty id");
        }
        let div_selector = Selector::parse("div").unwrap();
        let div = article.select(&div_selector).next().unwrap(); // this div may not exist, use unwrap in accident
        let a_selector = Selector::parse("a").unwrap();
        let a = div.select(&a_selector).next().unwrap();
        let link = a.value().attr("href"); // optional comic link
        let img_selector = Selector::parse("img").unwrap();
        let img = div.select(&img_selector).next().unwrap();
        let title = img.value().attr("title"); // optional comic title

        if let Some(comic_title) = title {
            //println!("{comic_title}");
            comic_info.title = String::from(comic_title);
        } else {
            println!("Empty title");
        }

        if let Some(comic_link) = link {
            //println!("{comic_link}");
            comic_info.link = String::from(comic_link);
        } else {
            println!("Empty link");
        }

        // write comic_info to comic set
        file.write_all("- id: ".as_bytes()).expect("e");
        file.write_all(comic_info.id.as_bytes()).expect("c");
        file.write_all("\n".as_bytes()).expect("j");

        file.write_all("  title: ".as_bytes()).expect("uu");
        file.write_all(comic_info.title.as_bytes()).expect("iii");
        file.write_all("\n".as_bytes()).expect("o");

        file.write_all("  link: ".as_bytes()).expect("pp");
        file.write_all(comic_info.link.as_bytes()).expect(";;");
        file.write_all("\n".as_bytes()).expect("ee");

        pb.inc(1);
    }
    pb.finish_with_message("all comic info loaded")
}


// establish ProgressSpinner, test cases only
fn gen_pb() {
    let spinner_style = ProgressStyle::default_spinner().tick_chars("⠁⠂⠄⡀⢀⠠⠐⠈ ");
    let pb = ProgressBar::new_spinner();
    pb.set_style(spinner_style);
    for _ in 0..1023 {
        pb.inc(1);
        thread::sleep(Duration::from_millis(5));
    }
    pb.finish_with_message("done");
}

// get comic jpg files from nyahentai.biz with selected link
fn get_pic(addr: String, id: String) {
    println!("fetch pic from addr: {}", addr);
    let resp = reqwest::blocking::get(addr).expect("bad parameter addr in get_pic");
    let content = resp.text().unwrap(); // source code of comic page
    /*
    let path = Path::new("D:\\NJU\\get_comic\\sample_section.html");
    let mut file = File::create(&path).unwrap();
    file.write(content.as_bytes()).unwrap();
    */
    let dir_path = String::from("D:\\NJU\\get_comic\\download\\") + &id;
    let mk = fs::create_dir(Path::new(&dir_path));

    match mk {
        Ok(()) => println!("mkdir {}", id),
        Err(e) => println!("{}, proceed anyway", e),
    }

    // generate pic list 
    let document = Html::parse_document(&content);
    let img_selector = Selector::parse("img").unwrap();
    let all_img = document.select(&img_selector);

    let mut img_num = 0;
    let mut pic_list = Vec::new();

    for img in all_img {
        let pic_link = img.value().attr("data-lazy-src");
        if let Some(valid_link) = pic_link {
            if valid_link.contains("cdn") {
                img_num = img_num + 1;
                //println!("{valid_link}");
                pic_list.push(String::from(valid_link));
            } else {
                // do nothing 
            }
        } else {
            // do nothig 
        }
    }

    let mut digit_num = 0;
    let mut tmp = img_num;

    while tmp > 0 {
        tmp = tmp / 10;
        digit_num = digit_num + 1;
    }

    let mut pic_cnt = 0;

    let pb = ProgressBar::new(img_num);

    for link in pic_list {
        pic_cnt = pic_cnt + 1;
        let mut digit_len = 0;
        let mut tmp = pic_cnt;
        while tmp > 0 {
            digit_len = digit_len + 1;
            tmp = tmp / 10;
        }
        let mut pic_name = pic_cnt.to_string();
        while digit_len < digit_num {
            pic_name = String::from("0") + &pic_name;
            digit_len = digit_len + 1;
        }

        //println!("{}: {}", pic_name, link);
        let pic_path = dir_path.clone() + &String::from("\\") + &pic_name + &String::from(".jpg");
        let mut pic = File::create(&Path::new(&pic_path)).unwrap();

        reqwest::blocking::get(link)
            .expect("bad picture addr")
            .copy_to(&mut pic)
            .unwrap();
    
        pb.inc(1);
    }
    pb.finish_with_message("all downloaded");
}

fn main() {
    //load_info(String::from("boudica"), 1); // do not run this function when testing pic-downloading function
    get_pic(String::from("https://nyahentai.biz/2022-boudica-orusuban-o-suru-boudica-x27-s-house-sitting.html"), String::from("post-128183"));
}
