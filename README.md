** HTTP сервер **

*1. Запустить сервер*
`python server.py`

*2. Произвести тестирование*
`wrk -t10 -c10 http://127.0.0.1:8080/`

При CI/CD проведен benchmark в .gihub/workflow/main.yml
