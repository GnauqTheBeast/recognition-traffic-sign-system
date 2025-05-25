package com.lcm.traffic_sign_service.controller;

import com.lcm.traffic_sign_service.entity.TrafficSignRequest;
import com.lcm.traffic_sign_service.entity.TrafficSign;
import com.lcm.traffic_sign_service.service.TrafficSignService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

@RestController
@RequestMapping("/api/traffic-signs")
public class TrafficSignController {

    private final TrafficSignService trafficSignService;

    @Autowired
    public TrafficSignController(TrafficSignService trafficSignService) {
        this.trafficSignService = trafficSignService;
    }


    @GetMapping
    public ResponseEntity<List<TrafficSign>> getAllTrafficSigns() {
        List<TrafficSign> trafficSigns = trafficSignService.getAllTrafficSigns();

        for (TrafficSign sign : trafficSigns) {
            // Giả sử bạn lưu trữ ảnh trong thư mục /uploads và có URL base là http://localhost:8080/
            String imageUrl = "http://localhost:8083" + sign.getImagePath();
            sign.setImagePath(imageUrl);
        }

        return new ResponseEntity<>(trafficSigns, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<TrafficSign> getTrafficSignById(@PathVariable Long id) {
        TrafficSign trafficSign = trafficSignService.getTrafficSignById(id);
        return new ResponseEntity<>(trafficSign, HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<?> addTrafficSign(
            @RequestParam("data") String jsonData,
            @RequestPart("image") MultipartFile imageFile) throws IOException {

        ObjectMapper mapper = new ObjectMapper();
        TrafficSignRequest data = mapper.readValue(jsonData, TrafficSignRequest.class);

        String uploadDir = "uploads/";
        Files.createDirectories(Paths.get(uploadDir));

        String filename = UUID.randomUUID() + "_" + imageFile.getOriginalFilename();
        Path filepath = Paths.get(uploadDir, filename);
        Files.write(filepath, imageFile.getBytes());

        TrafficSign sign = new TrafficSign();
        sign.setName(data.getName());
        sign.setDescription(data.getDescription());
        sign.setType(data.getType());
        sign.setXMin(data.getXMin());
        sign.setYMin(data.getYMin());
        sign.setXMax(data.getXMax());
        sign.setYMax(data.getYMax());
        sign.setImagePath("/uploads/" + filename);

        System.out.println("==== Received DTO ====");
        System.out.println(data);

        trafficSignService.createTrafficSign(sign);
        return ResponseEntity.ok("Uploaded successfully!");
    }

    // @PostMapping
    // public ResponseEntity<?> addTrafficSign(
    //         @RequestPart("data") TrafficSignRequest data,
    //         @RequestPart("image") MultipartFile imageFile) throws IOException {

    //     String uploadDir = "uploads/";
    //     Files.createDirectories(Paths.get(uploadDir));

    //     String filename = UUID.randomUUID() + "_" + imageFile.getOriginalFilename();
    //     Path filepath = Paths.get(uploadDir, filename);
    //     Files.write(filepath, imageFile.getBytes());

    //     TrafficSign sign = new TrafficSign();
    //     sign.setName(data.getName());
    //     sign.setDescription(data.getDescription());
    //     sign.setType(data.getType());
    //     sign.setXMin(data.getXMin());
    //     sign.setYMin(data.getYMin());
    //     sign.setXMax(data.getXMax());
    //     sign.setYMax(data.getYMax());
    //     sign.setImagePath("/uploads/" + filename);

    //     System.out.println("=======================Create Traffic Sign=======================");
    //     System.out.println(sign);

    //     trafficSignService.createTrafficSign(sign);
    //     return ResponseEntity.ok("Uploaded successfully!");
    // }

    // @PutMapping("/{id}")
    // public ResponseEntity<?> updateTrafficSign(
    //         @PathVariable Long id,
    //         @RequestBody TrafficSign trafficSign) {

    //     TrafficSign existingTrafficSign = trafficSignService.getTrafficSignById(id);
    //     if (existingTrafficSign == null) {
    //         return new ResponseEntity<>("Traffic sign not found", HttpStatus.NOT_FOUND);
    //     }

    //     boolean nameExists = trafficSignService.isNameExists(trafficSign.getName());
    //     if (nameExists && !existingTrafficSign.getName().equals(trafficSign.getName())) {
    //         return new ResponseEntity<>("Name already exists", HttpStatus.CONFLICT);
    //     }

    //     TrafficSign updatedTrafficSign = trafficSignService.updateTrafficSign(id, trafficSign);
    //     return new ResponseEntity<>(updatedTrafficSign, HttpStatus.OK);
    // }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateTrafficSign(
            @PathVariable Long id,
            @RequestParam("data") String jsonData,
            @RequestPart(value = "image", required = false) MultipartFile imageFile) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        TrafficSignRequest data = mapper.readValue(jsonData, TrafficSignRequest.class);

        TrafficSign existingTrafficSign = trafficSignService.getTrafficSignById(id);
        if (existingTrafficSign == null) {
            return new ResponseEntity<>("Traffic sign not found", HttpStatus.NOT_FOUND);
        }

        existingTrafficSign.setName(data.getName());
        existingTrafficSign.setDescription(data.getDescription());
        existingTrafficSign.setType(data.getType());
        existingTrafficSign.setXMin(data.getXMin());
        existingTrafficSign.setYMin(data.getYMin());
        existingTrafficSign.setXMax(data.getXMax());
        existingTrafficSign.setYMax(data.getYMax());

        if (imageFile != null && !imageFile.isEmpty()) {
            String uploadDir = "uploads/";
            Files.createDirectories(Paths.get(uploadDir));

            String filename = UUID.randomUUID() + "_" + imageFile.getOriginalFilename();
            Path filepath = Paths.get(uploadDir, filename);
            Files.write(filepath, imageFile.getBytes());

            existingTrafficSign.setImagePath("/uploads/" + filename);
        }

        TrafficSign updatedTrafficSign = trafficSignService.updateTrafficSign(id, existingTrafficSign);
        return new ResponseEntity<>(updatedTrafficSign, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTrafficSign(@PathVariable Long id) {
        trafficSignService.deleteTrafficSign(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
} 