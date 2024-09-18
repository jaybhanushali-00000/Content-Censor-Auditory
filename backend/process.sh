
cd backend
source virt/bin/activate
cd Code
pip3 install -r requirements.txt
mkdir ExtractedFiles
python3 audioExtract.py
cd ExtractedFiles
whisper "audio.mp3" --language English --fp16 False
cd ..
python3 MutingCensoredV2.py
python3 FinalStich.py
rm -r ExtractedFiles
cd ..
deactivate
echo "The output is in ExtractedFiles as Final_video.mp4"
