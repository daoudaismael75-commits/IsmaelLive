# IsmaelLive V1.9 — accès HTTPS privé

Ce simulateur ne diffuse pas de live public. Les spectateurs et cadeaux sont fictifs (badge SIM). La photo personnelle reste dans le navigateur. La caméra est affichée entière ; le fond flou comble les espaces. Android peut choisir l'objectif et ne pas fournir le réglage zoom. Le panneau de réglages affiche les dimensions et le zoom rapporté par le navigateur.

## Mac (test local)
`python3 server.py` (ou configuration XAI_API_KEY dans le terminal avant démarrage). L'adresse locale est http://localhost:8765. Ne pas utiliser --host 0.0.0.0 sans mot de passe.

## Render (Internet)
1. Crée un nouveau dépôt GitHub privé, ajoute le contenu de ce dossier IsmaelLive (pas le dossier parent). Pour les avatars facultatifs, lance `python3 install_avatars.py` avant l'envoi. Ne mets aucune clé API ni mot de passe dans le dépôt.
2. https://dashboard.render.com : New > Web Service, connecte ce dépôt. Runtime Python, Build Command `python -m py_compile server.py`, Start Command `python server.py --host 0.0.0.0 --port $PORT`, plan Free ou payant, Health Check Path `/healthz`.
3. Ajoute les variables LIVE_USER=ismael, LIVE_PASSWORD (mot de passe unique aléatoire d'au moins 16 caractères), XAI_API_KEY (clé neuve), facultativement XAI_MODEL (modèle compatible texte/image). LIVE_HOURLY_LIMIT=900 limite les appels par heure par instance ; ce n'est pas un plafond de facturation. Ne partage jamais la clé API.
4. Déploie. Ouvre l'URL HTTPS fournie par Render sur le Samsung, authentifie-toi et autorise la caméra et le micro. Réinstalle la PWA depuis Chrome pour la nouvelle adresse. Aucun USB/Mac requis après déploiement.
5. Le plan Free peut s'endormir après 15 minutes d'inactivité ; les crédits Grok restent payants selon le compte. Le serveur est destiné à un test personnel avec accès protégé. La reconnaissance vocale et Grok peuvent envoyer des données aux prestataires ; obtenir le consentement des personnes filmées.

Le service worker V1.9 supprime les anciens caches de cette application et n'intercepte plus les requêtes. Une nouvelle adresse HTTPS ne partage pas le cache de localhost. La V1.9 est affichée sur l'écran de préparation.

## Mise à jour d'un service existant
Conserver les variables Render. Remplacer les fichiers serveur et le dossier public en gardant l'arborescence. Build recommandé : `python -m py_compile server.py && (python3 install_avatars.py || echo "Portraits indisponibles : avatars illustrés actifs")`. Si l'ancien script échoue, le site fonctionne quand même. Ne pas envoyer de secrets dans le dépôt. Réinstaller le raccourci Chrome si nécessaire.
Dans l'écran de préparation, vérifier V1.9 et cliquer sur Tester la connexion Grok (texte fictif, appel API facturable). En live, ouvrir les réglages pour le zoom matériel et la latence. Le fond flou est agrandi mais jamais la vidéo principale. Si Android ne fournit pas le zoom, choisir un autre objectif dans les réglages. Les autorisations audio/image restent facultatives et doivent être données par les personnes filmées.
