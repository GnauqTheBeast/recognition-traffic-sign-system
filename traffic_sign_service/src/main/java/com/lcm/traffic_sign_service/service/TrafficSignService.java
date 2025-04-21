package com.lcm.traffic_sign_service.service;

import com.lcm.traffic_sign_service.entity.TrafficSign;

import java.util.List;

public interface TrafficSignService {
    List<TrafficSign> getAllTrafficSigns();
    TrafficSign getTrafficSignById(Long id);
    TrafficSign createTrafficSign(TrafficSign trafficSign);
    TrafficSign updateTrafficSign(Long id, TrafficSign trafficSign);
    void deleteTrafficSign(Long id);
    boolean isNameExists(String name);
}
