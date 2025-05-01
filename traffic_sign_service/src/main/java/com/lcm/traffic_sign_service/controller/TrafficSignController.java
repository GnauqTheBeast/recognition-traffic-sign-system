package com.lcm.traffic_sign_service.controller;

import com.lcm.traffic_sign_service.dto.TrafficSignRequest;
import com.lcm.traffic_sign_service.entity.TrafficSign;
import com.lcm.traffic_sign_service.service.TrafficSignService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

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

//    @GetMapping("/{imageName}")
//    public ResponseEntity<Resource> getImage(@PathVariable String imageName) {
//        try {
//            if (imageName.contains("..") || imageName.contains("/") || imageName.contains("\\")) {
//                return ResponseEntity.badRequest().build();
//            }
//
//            Path uploadDir = Paths.get("uploads").toAbsolutePath().normalize();
//            Path imagePath = uploadDir.resolve(imageName).normalize();
//
//            if (!imagePath.startsWith(uploadDir)) {
//                return ResponseEntity.badRequest().build();
//            }
//
//            Resource resource = new UrlResource(imagePath.toUri());
//
//            if (resource.exists() && resource.isReadable()) {
//                String contentType = determineContentType(imageName);
//
//                return ResponseEntity.ok()
//                        .contentType(MediaType.parseMediaType(contentType))
//                        .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + resource.getFilename() + "\"")
//                        .body(resource);
//            } else {
//                throw new FileNotFoundException("Image not found: " + imageName);
//            }
//        } catch (MalformedURLException e) {
//            throw new RuntimeException("Error: " + e.getMessage(), e);
//        } catch (FileNotFoundException e) {
//            return ResponseEntity.notFound().build();
//        }
//    }

    /**
     * Xác định Content-Type dựa vào phần mở rộng của file
     */
//    private String determineContentType(String filename) {
//        String extension = "";
//        int lastDotIndex = filename.lastIndexOf('.');
//        if (lastDotIndex > 0) {
//            extension = filename.substring(lastDotIndex + 1).toLowerCase();
//        }
//
//        switch (extension) {
//            case "jpg":
//            case "jpeg":
//                return "image/jpeg";
//            case "png":
//                return "image/png";
//            case "gif":
//                return "image/gif";
//            case "bmp":
//                return "image/bmp";
//            case "webp":
//                return "image/webp";
//            case "svg":
//                return "image/svg+xml";
//            default:
//                return "application/octet-stream";
//        }
//    }

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

//    @PostMapping
//    public ResponseEntity<?> createTrafficSign(@RequestBody TrafficSign trafficSign) {
//        boolean exists = trafficSignService.isNameExists(trafficSign.getName());
//        System.out.println(exists);
//        if (exists) {
//            return new ResponseEntity<>("Name already exists", HttpStatus.CONFLICT);
//        }
//
//        System.out.println(trafficSign);
//
//        TrafficSign createdTrafficSign = trafficSignService.createTrafficSign(trafficSign);
//        return new ResponseEntity<>(createdTrafficSign, HttpStatus.CREATED);
//    }

    @PostMapping
    public ResponseEntity<?> addTrafficSign(
            @RequestPart("data") TrafficSignRequest data,
            @RequestPart("image") MultipartFile imageFile) throws IOException {

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

        System.out.println("=======================Create Traffic Sign=======================");
        System.out.println(sign);

        trafficSignService.createTrafficSign(sign);
        return ResponseEntity.ok("Uploaded successfully!");
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateTrafficSign(
            @PathVariable Long id,
            @RequestBody TrafficSign trafficSign) {

        TrafficSign existingTrafficSign = trafficSignService.getTrafficSignById(id);
        if (existingTrafficSign == null) {
            return new ResponseEntity<>("Traffic sign not found", HttpStatus.NOT_FOUND);
        }

        boolean nameExists = trafficSignService.isNameExists(trafficSign.getName());
        if (nameExists && !existingTrafficSign.getName().equals(trafficSign.getName())) {
            return new ResponseEntity<>("Name already exists", HttpStatus.CONFLICT);
        }

        TrafficSign updatedTrafficSign = trafficSignService.updateTrafficSign(id, trafficSign);
        return new ResponseEntity<>(updatedTrafficSign, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTrafficSign(@PathVariable Long id) {
        trafficSignService.deleteTrafficSign(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
} 