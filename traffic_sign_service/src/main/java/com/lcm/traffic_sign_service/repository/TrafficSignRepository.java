package com.lcm.traffic_sign_service.repository;

import com.lcm.traffic_sign_service.entity.TrafficSign;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TrafficSignRepository extends JpaRepository<TrafficSign, Long> {
    boolean existsByName(String name);
} 