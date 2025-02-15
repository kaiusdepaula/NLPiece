<img src="readme_files/logo.png" alt="NLPiece logo" width="700">

**N**atural **L**anguage **P**rocessing onep**IECE** is a pretty suggestive name, but let me
simplify it even more: say you wish to investigate topics surrounding the enourmous story of One Piece.
How would you base your affirmations if not on you interpretation of the story?

If you're a One Piece fan, you know that Eiichiro Oda's storytelling 
goes far beyond a rubber-powered pirate, it's a masterpiece of world-building, 
philosophy, and adventure.

This project aims to extract text from every single volume of the *greatest 
story ever told* and dive deep into text analysis using contextual [Top2Vec](https://github.com/ddangelov/Top2Vec). 

I'll be leveraging the powerful [MagiV2]() transformer model to extract transcripts of the source material, 
storing everything on a plain text. After that, I'll provide a very extensive analysis using basic stuff, such as 
tf-idf on volumes and sagas. Not only that, I'll extract topics and provide embeddings for each volume of the story.

Not only it'll be possible to agreggate every text into volumes, Magiv2 gives us the possibility to aggregate into
a character level! Here is a great example of MagiV2 classification working:

<img src="readme_files/magiexample1.png" alt="MagiV2 example" width="350">

To make this even more exciting, I'll do my best to release both the 
dataset and my text analysis to the public, because great stories deserve great exploration. Stay tuned!

## Project Structure

I've developed a simple file structure that may be helpfull for anyone trying to replicate what I've done personally.
It goes as such:

```
.
├── character_images     # This is where I store character images.
│   ├East_Blue           # I found out working with sagas give out a best result in classification.
│   └...
├── data                 # This is where the source files go.
│   ├v001                # They get grouped by volumes.
│   │   ├page1.png        # Each volume has n amount of pages.
│   │   ├page2.png
│   │   └...
│   ├v002
│   └...
├── outputs              # This is where scans are stored after magiv2 does it's magic. (pun intended)
├── readme_files         # The only images I'm currently storing here at github.
├── src                  # Source code and functions.
├── transcripts          # The output of the extraction phase.
│   ├v001
│   │   └transcript.txt
│   ├v002
│   └...
├── pyproject.toml       # Use a pipenv manager to replicate the python modules used. (or even pip itself)
├── README.md            # This document.
└── unpack_manga.sh      # A shell script that I've developed to unzip my mangás into the file system I've explained.
```