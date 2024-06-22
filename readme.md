# True Readme
	
	fn load_info(keyword: String, page: u64)

this function simulated 'search' procedure in nyahentai.biz, with a keyword(searching result might be null, namely no relevant content can be found) and a page number(be careful if the page number is larger than existing numnbers of the keyword). Results will be save in [comic_set.yaml](./comic_set.yaml), refer to it for more information

	fn get_pic(addr: String, id: String)

addr is url of the comic you want to download, id is the post-id; both of them can be found in comic_set.yaml. Call this function, a folder named with post-id will be created in the 'download' directory, pictures will be saved there


# Logs

### 2024.5.31

  After implementing baisc functions through python packages, try to do the same thing with rust, like the zed ide I am using.

### 2024.6.4

  still learning rust. succeed in getting source code from nyahentai.biz, next will try to parse it and get comic_set like what I did in py-version.

### 2024.6.22

  finish get_pic_link function which extracts pictures from select comic addr
  
  finish get_pic function; 
  
  **to do**:

    add log function
    save all functions as a lib 