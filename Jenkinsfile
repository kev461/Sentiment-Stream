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
                // Descarga del código desde GitHub
                git branch: 'main', url: 'https://github.com/tu-usuario/SentimentStream.git'
            }
        }

        stage('Pruebas Dataset') {
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker run --rm -v "%WORKSPACE%:/app" python:3.11-slim ^
                sh -c "pip install pandas pymongo && python /app/modulos_datos/verificar_dataframe.py" ^
                > outputs\\logs\\dataset_test.log 2>&1
                '''
            }
        }

        stage('Prueba Mongo') {
            // Verificamos la conexión a MongoDB Atlas antes de levantar todo
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker run --rm -v "%WORKSPACE%:/app" -e MONGO_URI="%MONGO_URI%" python:3.11-slim ^
                sh -c "pip install pymongo && python /app/flujos/test_mongo.py" ^
                > outputs\\logs\\test_mongo.log 2>&1
                '''
            }
        }

        stage('Build & Up Infrastructure') {
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

        stage('Exponer URL (Bono)') {
            steps {
                echo "--- URL PÚBLICA DE NGROK ---"
                bat 'docker logs sentiment_ngrok'
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
