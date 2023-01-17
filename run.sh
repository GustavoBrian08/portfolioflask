#!/bin/bash
# primeiro crie o arquivo run.sh
# alterar permissão para o arquivo ser executado chmod 777 run.sh
# execute o arquivo para iniciar a aplicação flask ./run.sh
source auth/bin/activate
export FLASK_APP=app
export FLASK_DEBUG=True
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=81
export FLASK_ENV=development
echo "Executando a aplicação!"
sleep 3

sudo flask run