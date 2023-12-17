[![Project Videos Tests](https://github.com/fred1599/video_project/actions/workflows/project-tests.yml/badge.svg)](https://github.com/fred1599/video_project/actions/workflows/project-tests.yml)

# Video Processing Application

This application allows performing various operations on video files, such as format conversion, repair, and audio extraction.

## Installation

Ensure Python 3.10 and `ffmpeg` are installed on your system. If not, you can download and install them from their respective websites.

## Usage

The application is executed via the command line. Here are the different commands and options available:

### General Commands

- **Help**: To display help and see all available options, use:

`python3.10 -m video --help`


### Video Conversion

- **Convert a Video**: To convert a video to another format, use:

`python3.10 -m video --command convert --input <path_to_video> --output <output_format> [--quality <quality>]`

- `<path_to_video>`: Path of the source video file.
- `<output_format>`: Desired output format (e.g., mp4, avi).
- `<quality>`: Video quality (low, middle, high). Defaults to `middle`.

### Video Repair

- **Repair a Video**: To attempt to repair a corrupted video, use:

`python3.10 -m video --command repair --input <path_to_video>`

- `<path_to_video>`: Path of the video file to repair.

### Audio Extraction

- **Extract Audio from a Video**: To extract the audio track from a video, use:

`python3.10 -m video --command extract_audio --input <path_to_video> --output <audio_format>`

- `<path_to_video>`: Path of the source video file.
- `<audio_format>`: Desired audio format for extraction (e.g., mp3, wav).

## Supported Formats

- **Supported video formats**: mp4, avi, mkv, mov, flv, wmv.
- **Supported audio formats**: mp3, aac, wav, ogg, flac.

## Dependencies

- Python 3.10
- `ffmpeg`

## Contribuer au Projet

Nous accueillons avec plaisir les contributions de la communauté ! Si vous souhaitez contribuer au projet [video_project](https://github.com/fred1599/video_project), voici les étapes à suivre :

1. **Forker le Projet**  
   Commencez par forker le projet sur votre compte GitHub. Cela crée une copie personnelle du projet sur laquelle vous pouvez travailler. Vous pouvez forker le projet en cliquant sur le bouton "Fork" en haut à droite de la page du projet.

2. **Cloner le Fork**  
   Ensuite, clonez votre fork sur votre machine locale. Cela vous permettra de travailler sur le projet en local. Utilisez la commande :

`git clone https://github.com/votre-username/video_project.git`

Remplacez `votre-username` par votre nom d'utilisateur GitHub.

3. **Créer une Branche**  
Créez une nouvelle branche pour vos modifications. Cela aide à séparer vos contributions des autres et facilite la gestion des modifications. Par exemple :

`git checkout -b nom-de-votre-branche`

4. **Apporter vos Modifications**  
Effectuez vos modifications dans cette branche. Assurez-vous de suivre les conventions de codage du projet et d'ajouter des tests si nécessaire.

5. **Commit et Push**  
Après avoir effectué vos modifications, committez-les et poussez-les sur votre fork. Par exemple :

```bash
git commit -m "Ajout d'une nouvelle fonctionnalité"
git push origin nom-de-votre-branche
```

6. **Créer une Pull Request**  
Une fois vos modifications poussées sur votre fork, créez une pull request sur le dépôt principal. Allez sur la page GitHub de votre fork et cliquez sur "Pull Request", puis suivez les instructions pour soumettre votre pull request.

7. **Attendez la Revue**  
Votre pull request sera examinée par les mainteneurs du projet. Ils peuvent vous demander de faire des modifications supplémentaires. Une fois votre pull request approuvée, elle sera fusionnée dans le projet principal.

8. **Gardez votre Fork à Jour**  
Après avoir contribué, gardez votre fork à jour avec le dépôt principal. Vous pouvez le faire en configurant un remote "upstream" et en synchronisant régulièrement votre fork :

```bash
git remote add upstream https://github.com/fred1599/video_project.git
git fetch upstream
git checkout master
git merge upstream/master
```

Nous vous remercions pour votre contribution au projet !