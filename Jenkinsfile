pipeline {
    agent any

    environment {
        // Credenciales seguras inyectadas desde Jenkins
        MONGO_URI = credentials('MONGO_URI')
        MONGO_DB = credentials('MONGO_DB')
        MONGO_COLECCION = credentials('MONGO_COLECCION')
        NGROK_AUTHTOKEN = credentials('NGROK_AUTHTOKEN')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/Sentiment-Stream.git'
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Creamos el directorio de logs de forma segura
                    bat 'if not exist outputs\\logs mkdir outputs\\logs'
                    
                    // Usamos writeFile para evitar problemas con caracteres especiales (como & o ^) en los tokens
                    def envContent = """
MONGO_URI=${MONGO_URI}
MONGO_DB=${MONGO_DB}
MONGO_COLECCION=${MONGO_COLECCION}
NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN}
""".trim()
                    writeFile file: '.env', text: envContent
                    echo "Archivo .env creado exitosamente."
                }
            }
        }

        stage('Build Image') {
            steps {
                // Construimos la imagen base una sola vez para usarla en pruebas y despliegue
                bat 'docker build -t sentiment-stream-app .'
            }
        }

        stage('Pruebas Dataset') {
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker run --rm -v "%WORKSPACE%:/app" sentiment-stream-app ^
                python /app/modulos_datos/verificar_dataframe.py ^
                > outputs\\logs\\dataset_test.log 2>&1
                '''
            }
        }

        stage('Prueba Mongo') {
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker run --rm ^
                -e MONGO_URI="%MONGO_URI%" ^
                -e MONGO_DB="%MONGO_DB%" ^
                -e MONGO_COLECCION="%MONGO_COLECCION%" ^
                sentiment-stream-app ^
                python /app/flujos/test_mongo.py ^
                > outputs\\logs\\test_mongo.log 2>&1
                '''
            }
        }

        stage('Deploy Infrastructure') {
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker-compose down
                docker-compose up -d --build > outputs\\logs\\docker_compose_up.log 2>&1
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                script {
                    bat '''
                    if not exist outputs\\logs mkdir outputs\\logs
                    set /a intentos=0
                    :loop
                    set /a intentos+=1
                    curl -f http://localhost:5000/stats > outputs\\logs\\smoke_test.log 2>&1
                    if %errorlevel%==0 exit /b 0
                    if %intentos% GEQ 15 exit /b 1
                    ping 127.0.0.1 -n 4 >nul
                    goto loop
                    '''
                }
            }
        }

        stage('Exponer URL') {
            steps {
                echo "--- REVISANDO ESTADO DE NGROK ---"
                // Esperamos un poco a que ngrok intente conectar
                bat 'ping 127.0.0.1 -n 5 >nul'
                bat 'docker logs sentiment_ngrok'
                echo "--- API DE TÚNELES (JSON) ---"
                bat 'curl -s http://localhost:4040/api/tunnels'
            }
        }

        stage('Archivar') {
            steps {
                archiveArtifacts artifacts: 'outputs\\**\\*.*', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline completado. Revisar logs en los artefactos de Jenkins.'
        }
    }
}
