import face_recognition
import cv2, os, pickle, subprocess, sys

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 1920)
video_capture.set(4, 1080)
load_store = True
siren=True
prompt = raw_input("Have you uploaded your picture yet? ").endswith('n')
if not prompt:
	max_num = int(max([int(item.split('.')[0].split('person')[-1]) for item in os.listdir('.') if item.endswith('.jpg')]))+1
	print "\n\n"
	print "Please upload a high quality selfie to this directory ("+os.getcwd()+").\nMake sure it is a JPG.\n\nNAME IT person"+str(max_num)+".jpg.\n\nOnce you have done that, please edit this python file (wherestyler.py), and on line 25, edit the array known_face_names and add your name to the end."
	print 'For example, if my name was Donald, and known_face_names was ["Jordan", "Jordan", "AJ", "Tyler", "Tyler", "Tyler"], I would change it to ["Jordan", "Jordan", "AJ", "Tyler", "Tyler", "Tyler", "Donald"]'
	print 'Make sure you append it to the end. Once you have done that, rerun this program.'
	print "\n\n"
	os.remove("encodings.txt")
	sys.exit(0)

###NAME ARRAY BELOW###

known_face_names = ["Jordan", "Jordan", "AJ", "Tyler", "Tyler", "Tyler"]

###NAME ARRAY ABOVE###

screen = raw_input("Would you like to show the video output? ").startswith('y')
if load_store:
	if os.path.isfile("encodings.txt"):
		load_file = open("encodings.txt", "rb")
		known_face_encodings = pickle.load(load_file)
	else:
		print "Load file was not found... initializing new encodings"
		load_file = open("encodings.txt", "wb")
		known_face_encodings = [face_recognition.face_encodings(face_recognition.load_image_file("person"+str(num)+".jpg")) for num in range(1, len(known_face_names)+1)]
		known_face_encodings = [item[0] for item in known_face_encodings if item]
		pickle.dump(known_face_encodings, load_file)


face_locations = []
face_encodings = []
face_names = []
process_this_frame = 1

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame == 1:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if any([encoding.any() for encoding in matches]):
		for match in range(len(matches)):
			if matches[match].any():
				name = known_face_names[match]
				break

	    print name
            face_names.append(name)
	    print face_names
	    if "Tyler" in face_names:
		if not tyler_detected:
			if siren:
				os.system("say Tyler, kindly remove thine presence from my kinosphere")
			else:
				os.system("say Tyler is behind you")
		else:
			pass
		tyler_detected = True
	    else:
		tyler_detected = False

    process_this_frame+=1
    if process_this_frame >= 2:
	process_this_frame = 1

    if screen:
	    for (top, right, bottom, left), name in zip(face_locations, face_names):
	        top *= 4
	        right *= 4
	        bottom *= 4
	        left *= 4
	        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
	        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
	        font = cv2.FONT_HERSHEY_DUPLEX
	        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
	
	    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
