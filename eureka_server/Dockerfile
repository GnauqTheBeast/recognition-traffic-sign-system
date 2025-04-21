FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY target/eureka_server-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]

#FROM openjdk:11-jre-slim
#
## Set the working directory
#WORKDIR /app
#
## Copy the built jar file into the image
#COPY ./target/eureka_server-0.0.1-SNAPSHOT.jar /app/eureka_server.jar
#
## Expose the port the app will run on
#EXPOSE 8761
#
## Run the JAR file
#CMD ["java", "-jar", "eureka_server.jar"]