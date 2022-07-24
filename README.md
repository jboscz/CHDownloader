# CHDownloader

CHDownloader is a program used to download Clone Hero songs from Google Drive folders and archive files. Input a Google Drive folder or file link into the entry box and click 'Download'. CHDownloader will download, extract and move your song folder into your Clone Hero songs folder, or any folder you specify. 

## Getting Started

This is what you'll need to get started:

1. Python (proven working on 3.8.0 64-bit)
2. Install these [packages](./requirements.txt)
3. A Google Drive API key. Steps to acquiring below

### Acquiring a Google Drive API key
1. Navigate to [https://console.cloud.google.com](https://console.cloud.google.com/)
2. Click on "APIs and Services"
3. Click on "Create Project"
![Red arrow pointing to "Create Project"](https://imgur.com/bJVEysH.png)
4. After creating your project, click "Library"
![Red arrow pointing to "Library"](https://imgur.com/W85XjfC.png)
5. Search for "Google Drive API"
![Search bar with "google drive api" entered](https://imgur.com/QFoE4x2.png)
6. Click the first result and then click "Enable". After it is done, navigate to "Credentials"
![Arrow pointing to "Credentials"](https://imgur.com/sxpbCox.png)
7. At the top, click on "Create Credentials" and then click on "Service Account"
![2 arrows pointing to "Create Credentials" first, then "Service Account" second](https://imgur.com/w3WKG1z.png)
8. Create a service account using the menu that shows. Name it whatever
9. After creating a service account, click on its name in the "Service Accounts" section of the "Credentials" page
![Highlighted link to the Service Account](https://imgur.com/mt7MAob.png)
10. Click on "Keys" in the top menu, and then click on the "Add Key" drop down list. Click on "Create new key"
![Service Account menu showing the "create new key" drop down from the "Keys" section](https://imgur.com/zLqd66S.png)
11. Leave the format as "JSON". It will download the file to your computer, make sure you move its location to the directory of CHDownloader.
![Prompt showing downloaded file information](https://imgur.com/CgS8ICj.png)
12. After moving the file, rename it to simply "project.json".

You have successfully acquired your Google Drive API key. Don't share it, who knows what they can do with it (I sure don't)

I work on new features when I have time. If you have suggestions, additions, whatever create an issue/push request or email me (TODO: add email)
