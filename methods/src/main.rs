use reqwest;

//#[tokio::fetch_html]
async fn fetch_html(url: String) {
    match reqwest::get(url).await {
        Ok(resp) => {
            println!("Response Status: {}", resp.status());
            // 处理响应数据
            let content = resp.text().await;
            println!("body as follows:\n{content:?}");
        }
        Err(err) => println!("Error: {}", err),
    }
}

use scraper::{Html, Selector};

fn parse_html(html: &str) {
    let document = Html::parse_document(html);
    let selector = Selector::parse(".some-class").unwrap();

    for element in document.select(&selector) {
        let text = element.text().collect::<Vec<_>>().join(" ");
        println!("Text: {}", text);
    }
}

// 在主函数中调用 parse_html

// read yaml file to get configurations
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Config {
    base_url: String,
}

use tokio;

fn main() -> Result<(), serde_yml::Error> {
    // Serialize to YAML
    let config_str = include_str!("../../config.yaml");
    let config: Config = serde_yml::from_str(&config_str)?;
    println!("target addr: {}", config.base_url);
    // create future mode
    let fetch = fetch_html(config.base_url);
    // create a runtime and run on it
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(fetch);
    Ok(())
}
