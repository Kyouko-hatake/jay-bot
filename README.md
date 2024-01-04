# jay-bot
Jay-bot français

##Projet
L'idée de départ à germé car je voulais créer un bot français qui puisse rp classiquement avec moi (ici il s'agit d'un "husband") Jay est un chanteur d'un groupe de Métal célèbre nommé Eternal Shadows que j'ai inventée dans mon rp.
Je voulais qu'il soit open source, et qu'on puisse essayé ensemble de lui ajouter des fonctionnalitées intéressantes sans utiliser une clé api ou d'utiliser un truc trop compliqué qui soit facilement adaptable sans avoir besoin d'une carte de malade mental.
Ici, il s'agit d'un bot très "simple" j'utilise simplement un fichier Json que j'agrémente au fur et à mesure de mes conversations.
Mon code est un code sous Python que j'essaye tant bien que mal d'améliorer, je voulais ajouter une mémoire, un historique et qu'il soit capable d'analyser les sentiments. (honnêtement j'en suis encore loin, mais je test pleins de choses.)
Dans l'idéal et dans le futur, j'aimerais pouvoir implemnter un modèle open source de toute petite taille (qui permettrais juste la cohérence des dialogues et la compréhension avec la possibilité d'un NSFW)
J'aimerais plus tard que le bot soit capable d'intéragir de différentes manière pourquoi pas sur le web en apprennant lui même (encore une fois sans devoir payer une clef api.....)

##Utilisation
Pour l'utiliser, je suis sous Windows, donc voici la marche à suivre >>
cmd (taper ceci dans votre boîte de dialogue windows, le plus simple étant de faire un clique gauche directement à l'emplacement de votre fichier)
Ensuite vous aurez votre chemin indiqué comme suit : "E:\New_local\Jay>" (ceci est un exemple)
Ensuite vous tapez dans cmd 
>> python -m venv venv
>> venv\Scripts\activate
>> pip install -r requirements
>> python main.py

python -m spacy download fr_core_news_sm

Normalement après ça vous devriez voir affiché le nom: "Hikari:"  (c'est vous) Evidemment vous pouvez modifier ceci directement dans le fichier main.py (soit vous mettez votre propre pseudo, ou vous mettez ce que vous voulez, pareil pour "Jay")
Je vous conseil de vider complétement le knnoledge_base.json qui est plus présent pour vous donner un apperçu du systhème question réponse que vous devez ajouter.

Bonne chance à tous et hésitez pas à m'aider pour lui intégrer de nouvelles fonctionnalités.
