package com.lcm.traffic_sign_service.service;

import com.lcm.traffic_sign_service.entity.TrafficSign;
import com.lcm.traffic_sign_service.repository.TrafficSignRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TrafficSignServiceImpl implements TrafficSignService {

    private final TrafficSignRepository trafficSignRepository;

    @Autowired
    public TrafficSignServiceImpl(TrafficSignRepository trafficSignRepository) {
        this.trafficSignRepository = trafficSignRepository;
    }

    @Override
    public List<TrafficSign> getAllTrafficSigns() {
        return trafficSignRepository.findAll();
    }

    @Override
    public TrafficSign getTrafficSignById(Long id) {
        return trafficSignRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Traffic sign not found with id: " + id));
    }

    @Override
    public TrafficSign createTrafficSign(TrafficSign trafficSign) {
        if (trafficSignRepository.existsByName(trafficSign.getName())) {
            throw new DuplicateNameException("Traffic sign with name '" + trafficSign.getName() + "' already exists");
        }

        return trafficSignRepository.save(trafficSign);
    }

    @Override
    public TrafficSign updateTrafficSign(Long id, TrafficSign updatedTrafficSign) {
        TrafficSign existingTrafficSign = getTrafficSignById(id);
        
        existingTrafficSign.setName(updatedTrafficSign.getName());
        existingTrafficSign.setDescription(updatedTrafficSign.getDescription());
        existingTrafficSign.setImagePath(updatedTrafficSign.getImagePath());
        existingTrafficSign.setType(updatedTrafficSign.getType());
        
        return trafficSignRepository.save(existingTrafficSign);
    }

    @Override
    public void deleteTrafficSign(Long id) {
        if (!trafficSignRepository.existsById(id)) {
            throw new EntityNotFoundException("Traffic sign not found with id: " + id);
        }
        trafficSignRepository.deleteById(id);
    }

    @Override
    public boolean isNameExists(String name) {
        return trafficSignRepository.existsByName(name);
    }
}

