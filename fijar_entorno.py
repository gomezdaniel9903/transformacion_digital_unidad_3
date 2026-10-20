import subprocess,sys
from pathlib import Path
from importlib.metadata import version
lines=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True).splitlines()
lines=[s+'; sys_platform == "win32"' if s.lower().startswith('pywin32==') else s for s in lines]
Path('requirements.txt').write_text('\n'.join(lines)+'\n')
names=['fastapi','uvicorn','scikit-learn','pandas','numpy','scipy','joblib','pydantic']
Path('requirements-api.txt').write_text('\n'.join(n+'=='+version(n) for n in names)+'\n')
print('Versiones fijadas',len(lines))
