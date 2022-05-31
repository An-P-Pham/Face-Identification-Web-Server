An Pham

Python Version: 3.8

Libraries:
    check requirements.txt exact & total requirements from: (pip freeze > requirements.txt)
    SQL script is provided in /sql directory
    files within /dlib to support face_recognition
    files within /pyimagesearch for openCV
    xml file from /cascades for openCV
    /unknown directory for clients to upload or take a new photo
    Import Libraries:
        Flask: Light-weight web framework for quick web application development
        os: Allows us to move around directories when saving pictures
        werkzeug.utils: Allows the client to send files securely
        cv2: allows us to use webcam as well as recognizing faces for accurate input
        face_recognition: Identify the face to known training set
        pathlib: More tools for finding directory paths
        pymysql: Save images in binary in mySQL database
        logging: Provides important information if program throws exception

How to run:
    - Start the project at recieve_Data.py
        - This will be the main activity that calls modules from other files
        - Please run as localhost and use any other browser besides Internet Explorer (I recommend chrome)
        - Finally please wait about 7-10 seconds for the server to start, there's a lot of overhead because
          the server checks the database if data exits then preload image files to service the client faster

Program overview:
    - Before recieve_Data.py starts a flask server, it checks pymysql database for any photos that are not
        inside /known directory, which is the training set of photos. After check sql for any possible saves
        it'll load the image encoding into runtime memory
    - Afterwards the client has a choice to either take a new photo or upload an existing one
    - Both methods are redirected towards their respective url to handle the request; however
      both eventually call access control. upload_photo uses the os library & werkzeug for a
      secured file transfer then an upload, while capture_photo calls the WebCam global object
      save a frame from the video feed
    - Afterwards, both request calls access control where the program calls detect_unknown within
      access_control.py which will send back a message to the client of either "No Matches" or
      "Matched: {client's name}"
    - A more indepth and detailed overview of the project can be seen in the .pdf file

Resources:
    - Special thank you for the people who have posted online guides and tutorials and for helping me
      understand how to implement.
      - Streaming video onto web via OpenCV:
            https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
      - Converting images to binary files & saving it into the mySQL database:
            https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/
      - USC ITP 499 instructors and teaching assistants

