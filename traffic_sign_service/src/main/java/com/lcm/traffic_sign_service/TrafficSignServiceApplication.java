package com.lcm.traffic_sign_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.context.annotation.Bean;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@SpringBootApplication
@EnableDiscoveryClient
public class TrafficSignServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(TrafficSignServiceApplication.class, args);
    }
}
