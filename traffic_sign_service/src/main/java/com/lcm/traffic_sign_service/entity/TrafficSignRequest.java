package com.lcm.traffic_sign_service.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TrafficSignRequest {
    private String name;
    private String description;
    private TrafficSign.TrafficSignType type;

    @JsonProperty("xMin")
    private double xMin;

    @JsonProperty("yMin")
    private double yMin;

    @JsonProperty("xMax")
    private double xMax;

    @JsonProperty("yMax")
    private double yMax;
}
