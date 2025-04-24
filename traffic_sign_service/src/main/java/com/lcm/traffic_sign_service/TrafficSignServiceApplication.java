package com.lcm.traffic_sign_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class TrafficSignServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(TrafficSignServiceApplication.class, args);
    }
}
