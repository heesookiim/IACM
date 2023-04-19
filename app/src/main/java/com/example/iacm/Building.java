package com.example.iacm;

import android.graphics.Color;

import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Polygon;
import com.google.android.gms.maps.model.PolygonOptions;

import java.util.ArrayList;

public class Building {
    private String buildingName;
    private String buildingCode;
    private ArrayList<LatLng> coordinates;
    private Polygon buildingPolygon;
    private PolygonOptions buildingPolygonOptions;

    private ArrayList<Entrance> entrances;
    private ArrayList<Bathroom> bathrooms;

    private int selectedFloor;

    private int num_floors;

    private static int width = 1;

    public Building(String buildingName, String buildingCode, ArrayList<LatLng> coordinates) {
        this.buildingName = buildingName;
        this.buildingCode = buildingCode;
        this.coordinates = coordinates;

        this.buildingPolygonOptions = new PolygonOptions()
                .strokeColor(Color.GRAY)
                .strokeWidth(width)
                .fillColor(Color.LTGRAY);

        for(int i = 0; i < coordinates.size(); i++) {
            buildingPolygonOptions.add(coordinates.get(i));
        }

        //buildingPolygon = new Polygon(buildingPolygonOptions);

        entrances = new ArrayList<>();
        bathrooms = new ArrayList<>();

        selectedFloor = 0;
        num_floors = 0;
    }

    public String getBuildingName() {
        return buildingName;
    }

    public String getBuildingCode() {
        return buildingCode;
    }

    public ArrayList<LatLng> getCoordinates() {
        return coordinates;
    }

    public Polygon getBuildingPolygon() {
        return buildingPolygon;
    }

    public void setBuildingPolygon(Polygon polygon) {
        buildingPolygon = polygon;
    }

    public PolygonOptions getBuildingPolygonOptions() {
        return buildingPolygonOptions;
    }

    public void addEntrance(Entrance entrance) {
        entrances.add(entrance);
    }

    public void addBathroom(Bathroom bathroom) {
        bathrooms.add(bathroom);
        if (bathroom.getLevel() > num_floors) {
            num_floors = bathroom.getLevel();
        }
    }

    public ArrayList<Entrance> getEntrances() {
        return entrances;
    }

    public ArrayList<Bathroom> getBathrooms() {
        return bathrooms;
    }

    public int getNumberOfFloors() {
        return num_floors;
    }

    public void setSelectedFloor(int floor) {
        if (selectedFloor == floor) {
            return;
        }
        if (selectedFloor == 0) {
            for (Entrance entrance : entrances) {
                entrance.getEntrancePolygon().setVisible(false);
                //System.out.println("Invisible entrance " + entrance);
            }
        }
        else if (floor == 0) {
            for (Entrance entrance : entrances) {
                entrance.getEntrancePolygon().setVisible(true);
                //System.out.println("Visible entrance " + entrance);
            }
        }
        for (Bathroom bathroom : bathrooms) {
            if (bathroom.getLevel() != floor) {
                bathroom.getBathroomPolygon().setVisible(false);
                //System.out.println("Invisible bathroom " + bathroom);
            }
            else {
                bathroom.getBathroomPolygon().setVisible(true);
                //System.out.println("Visible bathroom " + bathroom);
            }
        }
        selectedFloor = floor;
    }

    public void setFloorToZero() {
        for (Entrance entrance : entrances) {
            entrance.getEntrancePolygon().setVisible(true);
            //System.out.println("Visible entrance " + entrance);
        }
        for (Bathroom bathroom : bathrooms) {
            if (bathroom.getLevel() != 0) {
                bathroom.getBathroomPolygon().setVisible(false);
                //System.out.println("Invisible bathroom " + bathroom);
            }
            else {
                bathroom.getBathroomPolygon().setVisible(true);
                //System.out.println("Visible bathroom " + bathroom);
            }
        }
        selectedFloor = 0;
    }
}
