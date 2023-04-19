package com.example.iacm;

import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Polygon;
import com.google.android.gms.maps.model.PolygonOptions;

import java.util.ArrayList;

public class Bathroom {
    private ArrayList<LatLng> coordinates;
    private Boolean accessible;
    private Integer level;
    private String buildingCode;
    private String ID;
    private PolygonOptions bathroomPolygonOptions;
    private Polygon bathroomPolygon;
    private static int width = 1;

    public Bathroom(String ID, Integer level, String buildingCode, ArrayList coordinates, Boolean accessible){
        this.ID = ID;
        this.level = level;
        this.buildingCode = buildingCode;
        this.accessible = accessible;
        this.coordinates = coordinates;

        if(accessible == true) {
            this.bathroomPolygonOptions = new PolygonOptions()
                    .strokeColor(0xFF44BB99)
                    .strokeWidth(width)
                    .fillColor(0xFF44BB99);
        }else{
            this.bathroomPolygonOptions = new PolygonOptions()
                    .strokeColor(0xFFF2D98D)
                    .strokeWidth(width)
                    .fillColor(0xFFF2D98D);
        }

        for(int i = 0; i < coordinates.size(); i++) {
            bathroomPolygonOptions.add((LatLng) coordinates.get(i));
        }
    }
    public String getID() {
        return ID;
    }

    public String getBuildingCode() {
        return buildingCode;
    }
    public Integer getLevel() {
        return level;
    }
    public ArrayList<LatLng> getCoordinates() {
        return coordinates;
    }
    public Boolean getAccessible() {return accessible;}
    public PolygonOptions getBathroomPolygonOptions() {
        return bathroomPolygonOptions;
    }

    public Polygon getBathroomPolygon() {
        return bathroomPolygon;
    }

    public void setBathroomPolygon(Polygon polygon) {
        bathroomPolygon = polygon;
    }

}
