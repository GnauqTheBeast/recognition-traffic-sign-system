package com.lcm.traffic_sign_service.entity;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonValue;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Entity
@Table(name = "traffic_signs")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class TrafficSign {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String description;

    @Column(name = "imagePath")
    private String imagePath;

    @Column()
    @JsonProperty("xMin")
    private double xMin;

    @Column()
    @JsonProperty("yMin")
    private double yMin;

    @Column()
    @JsonProperty("xMax")
    private double xMax;

    @Column()
    @JsonProperty("yMax")
    private double yMax;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TrafficSignType type;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "createdAt", updatable = false)
    private Date createdAt;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "updatedAt")
    private Date updatedAt;

    public enum TrafficSignType {
        WARNING,
        PROHIBITION,
        INFORMATION;

        @JsonCreator
        public static TrafficSignType fromString(String value) {
            return TrafficSignType.valueOf(value.toUpperCase());
        }

        @JsonValue
        public String toValue() {
            return this.name().toLowerCase();
        }
    }

    @PrePersist
    protected void onCreate() {
        Date now = new Date();
        createdAt = now;
        updatedAt = now;
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = new Date();
    }
}
