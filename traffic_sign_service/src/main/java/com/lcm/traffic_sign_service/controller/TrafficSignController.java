package com.lcm.traffic_sign_service.controller;

import com.lcm.traffic_sign_service.entity.TrafficSign;
import com.lcm.traffic_sign_service.service.TrafficSignService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
        return new ResponseEntity<>(trafficSigns, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<TrafficSign> getTrafficSignById(@PathVariable Long id) {
        TrafficSign trafficSign = trafficSignService.getTrafficSignById(id);
        return new ResponseEntity<>(trafficSign, HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<?> createTrafficSign(@RequestBody TrafficSign trafficSign) {
        boolean exists = trafficSignService.isNameExists(trafficSign.getName());
        System.out.println(exists);
        if (exists) {
            return new ResponseEntity<>("Name already exists", HttpStatus.CONFLICT);
        }

        TrafficSign createdTrafficSign = trafficSignService.createTrafficSign(trafficSign);
        return new ResponseEntity<>(createdTrafficSign, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<TrafficSign> updateTrafficSign(
            @PathVariable Long id,
            @RequestBody TrafficSign trafficSign) {
        TrafficSign updatedTrafficSign = trafficSignService.updateTrafficSign(id, trafficSign);
        return new ResponseEntity<>(updatedTrafficSign, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTrafficSign(@PathVariable Long id) {
        trafficSignService.deleteTrafficSign(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
} 