from processing_upload import process_uploaded_file

print("Starting...")

chunks = process_uploaded_file(
    r"C:/Users\Anushka\Downloads/Loops in Java ｜ Java Placement Full Course ｜ Lecture 4 [0r1SfRoLuzU] (2) (mp3cut.net) (1).mp3",
    "4",
    "Loops"
)

print(chunks)