FROM eclipse-temurin:17-jdk-alpine
WORKDIR /backend
COPY . .
RUN ./mvnw clean package -DskipTests
EXPOSE 8080
CMD ["java", "-jar", "target/circus_porfolio_backend.jar"]