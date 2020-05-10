# Notion Search
This workflow is so simple and useful to find contents by text.
You know, there is quick search function in Notion.
So this workflow uses the function, actually un-officially API.

# How to Use
First of all, you find your token value.
Please refer to followings:
1. Please open Notion in your web browser.
2. Go to develop mode(chrome in osx, <kbd>cmd</kbd> + <kbd>opt</kbd> + <kbd>i</kbd>).
3. Go to 'Network' tab.
4. Seek 'https://www.notion.so/api/v3/getUserSharedPages' and see 'cookie'.
5. You can find `token_v2` value.

Please refer to this [page](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/README.md). 

## Initialize
You should initialize with setting token value.  
Default keyword is `0nt-init`, type it in Alfred.

## Search Contents
After initializing, you can search contents by text.     
Just type `0nt [text what you want to search]` in Alfred.

* You can see `created_itme` of page if you <kbd>ctrl</kbd>.
* You can see `tags` of page if you <kbd>cmd</kbd>.
* You can redirect to page in Web browser if you <kbd>ctrl</kbd> + <kbd>enter</kbd>.
* You can redirect to page in Notion Application if you <kbd>enter</kbd>

## Refresh Token
If you set mis-token, you can refresh your token.  
Type `0nt-re-init`.

# Contribution
If you have any questions, you can comment it in [Issues](https://github.com/spearkkk/alfred-workflow/issues).

# Reference
* [Workflow for Python](https://github.com/deanishe/alfred-workflow)
* [Original Notion Search Workflow](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/README.md)
  