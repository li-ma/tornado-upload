tornado-upload
==============

This is the demonstration for Tornado and Plupload integration, which supports multi-functional(also very stable) file uploading solution via web.

Installation
------------
1. First you need to install Tornado 3.1.1 by hand.
2. Execute the script: run.sh.
3. It will start the web server on port 8888.
4. Input '4321' as the only password from your web broswer.
5. You can upload any image files from web now.
6. The file will be stored in tmp directory of your project root directory.

Tornado Overview
----------------
Tornado is a Python web framework and asynchronous networking library. By using non-blocking network I/O, Tornado can scale to tens of thousands of open connections, making it ideal for long polling, WebSockets, and other applications, like file uploading, that require a long-lived connection to each user.

Official Website: http://www.tornadoweb.org

Plupload Overview
-----------------
Plupload is a fasinating web-based file uploader. It supports:
1. Multiple Runtime Plugins, like HTML5, Flash, Silverlight and traditional HTML4.
2. Drag'n'Drop Files from Desktop
3. Shrink Images on Client-Side
4. Upload in Chunks
5. Translated to 30+ Languages

Official Website: http://www.plupload.com

