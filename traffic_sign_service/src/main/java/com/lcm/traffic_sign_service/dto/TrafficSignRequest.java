package com.lcm.traffic_sign_service.dto;

import com.lcm.traffic_sign_service.entity.TrafficSign;
import lombok.Getter;
import lombok.Setter;

public class TrafficSignRequest {
    // Getters
    @Setter
    @Getter
    private String name;
    @Getter
    @Setter
    private String description;
    @Getter
    private TrafficSign.TrafficSignType type;
    private double xMin;
    private double yMin;
    private double xMax;
    private double yMax;

    public double getXMin() {
        return xMin;
    }

    public double getYMin() {
        return yMin;
    }

    public double getXMax() {
        return xMax;
    }

    public double getYMax() {
        return yMax;
    }

    public void setType(String type) {
        this.type = TrafficSign.TrafficSignType.valueOf(type);
    }

    public void setXMin(double xMin) {
        this.xMin = xMin;
    }

    public void setYMin(double yMin) {
        this.yMin = yMin;
    }

    public void setXMax(double xMax) {
        this.xMax = xMax;
    }

    public void setYMax(double yMax) {
        this.yMax = yMax;
    }
}
