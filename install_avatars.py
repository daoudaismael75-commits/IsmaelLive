#!/usr/bin/env python3
"""Download synthetic portraits for a clearly labelled fictional audience."""
from pathlib import Path, PurePosixPath
import tempfile, subprocess, zipfile, re, sys
ROOT=Path(__file__).resolve().parent/'public'/'avatars'
URL='https://codeload.github.com/TheTechBasket/personified/zip/refs/heads/main'

def install():
    ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        archive=Path(tmp)/'portraits.zip'
        print('Téléchargement des portraits synthétiques Personified…',flush=True)
        subprocess.run(['curl','--fail','--location','--retry','2','--connect-timeout','20','--max-time','240','--max-filesize','200000000','--output',str(archive),URL],check=True)
        with zipfile.ZipFile(archive) as z:
            found={}
            for item in z.infolist():
                p=PurePosixPath(item.filename)
                if len(p.parts)==4 and p.parts[1:3]==('img','128') and re.fullmatch(r'\d{4,6}\.webp',p.name) and 0<item.file_size<300000:
                    b=z.read(item)
                    if b[:4]==b'RIFF' and b[8:12]==b'WEBP':found[p.name]=b
            if not found:raise RuntimeError('Aucun portrait valide trouvé dans la collection.')
            license_data=None
            for item in z.infolist():
                if item.filename.count('/')==1 and item.filename.endswith('/LICENSE.md') and item.file_size<100000:
                    license_data=z.read(item);break
            if not license_data:raise RuntimeError('Licence de la collection introuvable.')
            (ROOT/'LICENSE.txt').write_bytes(license_data)
            for name,b in found.items():(ROOT/name).write_bytes(b)
        print(f'{len(found)} portraits installés localement. Redémarre le serveur.',flush=True)
if __name__=='__main__':
    try:install()
    except Exception as e:print('Installation impossible :',e,file=sys.stderr);sys.exit(1)
