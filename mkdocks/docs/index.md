# Welcome to DN-Sync

For the source code visit [my github page.](https://github.com/MaximKabaev/dropbox-to-notion-sync)

# Set up

## Dropbox

### 1. Organisation

Create a new folder in the root directory called `ToNotion`. There you can create other folders that will be the tags in notion. 
> **_Do not_** create multiple layers because that will not work.

### 2. Dropbox app
Now we need to create an app in Dropbox for the API. Follow this [link](https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps) and click **_create app_**.
Choose the options and name your app. The name does not matter just make sure you can recodnise it.

If you want options that will minimise your steps for the set up, follow [these steps.](https://scribehow.com/shared/Dropbox_Workflow__-8hTCKwbRcCj4MI50TI0wQ)

Now we need to give the premission to an app. You can turn them on cause it's your app. [Here are the steps to follow](https://scribehow.com/shared/Dropbox_Workflow__87pfhjPjQTKTwU_4qbvUnQ).

## Notion

### 3. Creating Notion integration

Follow [these steps](https://scribehow.com/shared/Notion_Workflow__Vok4S0bwRmqOtX3Y9Nmh8A) to create the integration

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
