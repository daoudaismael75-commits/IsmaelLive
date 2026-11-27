# Ismael Daouda Live — V1.7
Application web installable (PWA) pour entraînement personnel. Interface inspirée des lives mobiles, non affiliée à Instagram. Le public est fictif : aucune vidéo n'est diffusée, aucune connexion Instagram nécessaire. Les identités sont des pseudonymes inventés et les avatars peuvent utiliser des portraits synthétiques.

## Mac / ordinateur
1. Décompresser le ZIP. Ouvrir un terminal dans le dossier `IsmaelLive`.
2. Exécuter `python3 server.py` (Python 3.9+ ; aucune dépendance externe).
3. Ouvrir http://localhost:8765 dans Chrome. Choisir une durée de montée, la langue puis Démarrer le live. Autoriser caméra/micro si demandé. Le mode Tester sans caméra ne demande aucune permission.
4. Ctrl+C dans le terminal arrête le serveur.

## Android (Samsung) — installation PWA via USB, sans héberger sur Internet
L'accès caméra exige un contexte sécurisé : `localhost` ou HTTPS de confiance. Une adresse IP LAN en HTTP ne suffit généralement pas.
1. Installer Android Platform Tools depuis https://developer.android.com/tools/releases/platform-tools sur le Mac. Si Homebrew est déjà présent : `brew install --cask android-platform-tools`.
2. Sur Samsung : Paramètres > À propos du téléphone > Informations sur le logiciel > appuyer 7 fois sur Numéro de version. Dans Options de développement, activer Débogage USB.
3. Connecter le téléphone au Mac par câble USB de données et autoriser le débogage sur le téléphone.
4. En laissant `python3 server.py` tourner sur le Mac, ouvrir un second terminal et exécuter `adb devices`, puis `adb reverse tcp:8765 tcp:8765`.
5. Sur le téléphone, ouvrir Chrome à `http://localhost:8765`. Dans le menu Chrome, sélectionner Ajouter à l'écran d'accueil / Installer l'application (libellé variable). Accepter les permissions caméra/micro au démarrage du live.
6. Pour utiliser Grok depuis le téléphone via USB, conserver le serveur actif et la connexion USB. L'application peut conserver ses ressources statiques hors ligne, mais les requêtes IA nécessitent le serveur. Répéter `adb reverse` si nécessaire à la reconnexion. Désactiver le débogage USB après les tests.

## Grok (optionnel)
Créer une clé API xAI via https://console.x.ai/ (facturation API indépendante de l'abonnement Grok). Ne pas inscrire la clé dans le JavaScript. Arrêter le serveur et le relancer dans le terminal :
```bash
read -s 'XAI_API_KEY?Clé xAI : '; export XAI_API_KEY; echo
python3 server.py
```
La commande `read` ci-dessus utilise zsh (Mac). Sous bash : `read -rsp 'Clé xAI : ' XAI_API_KEY; export XAI_API_KEY; echo`.
Sur l'écran de démarrage, activer séparément Grok paroles et Grok images. La reconnaissance vocale est fournie par Chrome/Web Speech et peut dépendre d'un service réseau. Grok reçoit le texte transcrit et/ou une image JPEG réduite (environ toutes les 14 secondes si une demande précédente n'est pas en cours). La clé ne quitte pas le serveur local. Le serveur demande `store:false` à xAI mais les politiques du fournisseur s'appliquent. Aucun fichier audio/vidéo n'est enregistré par l'application. Les appels sont payants selon la tarification xAI. Modèle par défaut : `grok-4.7`, configurable via `XAI_MODEL`.

## Comportement
- Public : progression avec variations de 0 jusqu'à 34 500 sur 3, 10 ou 20 minutes, puis variation entre 32 600 et 34 500. Aucun dépassement du maximum.
- Commentaires locaux français/anglais avec quelques réactions à des mots-clés de la transcription ; Grok apporte le contexte plus avancé.
- Caméra avant/arrière, réactions animées, micro marche/arrêt, commentaires saisis, fin de live avec statistiques.
- Les commentaires et spectateurs sont fictifs ; l'application le précise au démarrage, dans les réglages et dans le récapitulatif, sans bannière permanente sur le live.
- La V1 ne contient pas d'APK natif, de diffusion, ni de vrais profils. Elle n'a pas été testée sur un téléphone physique ni avec une clé API réelle.

## Mise à jour V1.1
- Le démarrage demande le plein écran au navigateur ; bouton Plein écran disponible dans Réglages. Le manifeste demande aussi le mode fullscreen à Android.
- La caméra conserve le cadrage intégral (object-fit: contain), sans recadrage CSS. Des bandes sombres peuvent apparaître si les proportions diffèrent. Le zoom matériel 1× est demandé uniquement si le navigateur le propose.
- Après remplacement des fichiers, redémarrer le serveur, recharger la page sur le téléphone et relancer le live. Si nécessaire, réinstaller le raccourci PWA.
- Les changements n’ont pas été testés sur un téléphone physique.

## Mise à jour V1.2 — cadeaux virtuels
- Option activée par défaut, désactivable avant le live. Aucun paiement, aucune transaction ou collecte d'argent réelle. Les montants sont fictifs et identifiés à l'écran.
- Cadeaux spontanés après 18 à 40 secondes, puis à intervalles variables.
- Une demande de soutien reconnue par la transcription ou saisie dans le champ de commentaire déclenche 2 à 3 cadeaux, avec un délai de 25 secondes entre demandes. Exemples : « Les gars, il faut me supporter », « Soutenez-moi », « Envoyez des cadeaux », « Support me ». La reconnaissance locale ne nécessite pas Grok, mais le microphone du navigateur doit fonctionner.
- Récapitulatif du nombre de cadeaux et du montant fictif, remis à zéro à chaque live.
- V1.2 conserve le plein écran et la demande de zoom 1× de V1.1.

## V1.3
- Public fictif renouvelé : plusieurs milliers de pseudonymes générés localement et tirés sans remise par cycle. Les cadeaux réutilisent leur propre pseudo dans le commentaire associé.
- Progression graduelle sans recul avant 34 500, puis fluctuations de faible amplitude plafonnées. Choix de 3, 10, 20 ou 30 minutes.
- Cache PWA versionné ; plein écran conservé. Grok optionnel : clé API et consentement nécessaires.

## V1.4
Choisis une photo de profil avant le live (recadrée localement, conservée sur cet appareil, supprimable). La photo de profil n'est pas envoyée à Grok. Active séparément les options Grok paroles et images avant le live. Le navigateur transcrit silencieusement; la reconnaissance vocale peut dépendre d'un service externe. Grok reçoit le texte et/ou une image JPEG réduite toutes les ~14 secondes si autorisé; aucun son de réponse. Les captures et transcriptions cessent à la fin du live; les requêtes en cours déjà envoyées peuvent être traitées. Le traitement est suspendu lorsque la page est masquée. Vérifie l'état dans Réglages. Ne filme pas les autres sans leur accord. Le compteur et les cadeaux demeurent fictifs.

## V1.5
- Par défaut, aperçu vidéo bord à bord (recadrage CSS possible) avec zoom matériel 1× demandé si disponible. Option image entière si préférable.
- Montée sur 60 minutes par défaut, 30/90/120 min disponibles, progression accélérée doucement et plafonnée.
- Grok 4.3 sans raisonnement par défaut, envoi déclenché par la transcription, intervalle minimal 2,5 s, image seule toutes les ~5 s si autorisée. Une requête à la fois, délai réseau variable, pause en cas d’erreur. Les premiers commentaires IA sont affichés dès réception. Appels potentiellement payants.
- Consentements et absence de diffusion publique conservés. Les images et textes autorisés sont envoyés au fournisseur; pas de réponse audio.
- Réglages du live : état Grok et durée de dernière réponse, état micro, cadrage.

## V1.6 — Photos des spectateurs
Exécute `python3 install_avatars.py` depuis le dossier IsmaelLive avant de démarrer le serveur. Cette commande télécharge la collection Personified (https://github.com/TheTechBasket/personified), extrait uniquement les portraits WebP 128 px et conserve sa licence. Les portraits sont servis localement, sans accès à Instagram ni requête externe pendant le live. Les visages sont synthétiques et réservés à un public clairement fictif. Un pseudonyme conserve le même portrait tant que la collection ne change pas. Des portraits peuvent être partagés par plusieurs pseudonymes. Sans téléchargement ou si une image échoue, les initiales restent visibles.

La mention sous le profil est retirée ; un indicateur Démo reste à droite, et le public fictif est expliqué au démarrage, dans les réglages et le récapitulatif.

Le compteur progresse lentement vers 34 500 (60 min par défaut) avec des vagues de hausses et baisses avant le maximum, puis oscille entre 32 600 et 34 500. Les durées sont approximatives. Les portraits ne sont pas inclus dans le ZIP et nécessitent une installation séparée.

## V1.7
Pastille Démo supprimée du haut du live, badge LIVE simple. Le caractère fictif du public reste expliqué avant et après le live, dans les réglages et sur les cadeaux. Choix de langue du micro indépendant des commentaires (français ou anglais). Priorité aux paroles récentes, stabilité des fragments de transcription, requêtes espacées d'au moins 1,8 s, captures visuelles environ toutes les 4 s si activées. Grok est invité à commenter les conversations et à complimenter respectueusement les amis ou groupes présents, sans deviner leur identité ou inventer des détails. Les personnes filmées doivent consentir à l'envoi d'images. La vitesse dépend du navigateur, du réseau et de l'API; compréhension et compliments non garantis. Les portraits restent disponibles après installation via install_avatars.py.

Caméra : image entière sans recadrage par défaut, zoom matériel 1× si disponible. Le fond flou remplit les espaces inutilisés sans agrandir le visage dans l’image principale. Le mode bord à bord avec recadrage reste optionnel. Le rendu physique et la disponibilité des contraintes vidéo dépendent du téléphone.
