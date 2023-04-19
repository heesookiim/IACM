package com.example.iacm;

import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Polygon;
import com.google.android.gms.maps.model.PolygonOptions;

import java.util.ArrayList;

public class Entrance {
    private String entranceCode;
    private ArrayList<LatLng> coordinates;
    private PolygonOptions entrancePolygonOptions;
    private Polygon entrancePolygon;
    private boolean isAccessible;
    private static int width = 1;

    public Entrance(String entranceCode, ArrayList<LatLng> coordinates, boolean isAccessible) {
        this.entranceCode = entranceCode;
        this.coordinates = coordinates;
        this.isAccessible = isAccessible;

        entrancePolygonOptions = new PolygonOptions()
                .strokeWidth(width);

        if (this.isAccessible) {
            entrancePolygonOptions.strokeColor(0xFF77ABD9);
            entrancePolygonOptions.fillColor(0xFF77ABD9);
        } else {
            entrancePolygonOptions.strokeColor(0xFFF2836B);
            entrancePolygonOptions.fillColor(0xFFF2836B);
        }

        int numCoordinates = coordinates.size();

        for (int i = 0; i < numCoordinates; i++) {
            entrancePolygonOptions.add(coordinates.get(i));
        }
    }

    public String getEntranceCode() {
        return entranceCode;
    }

    public ArrayList<LatLng> getCoordinates() {
        return coordinates;
    }

    public Polygon getEntrancePolygon() {
        return entrancePolygon;
    }

    public PolygonOptions getEntrancePolygonOptions() { return entrancePolygonOptions; }

    public void setEntrancePolygon(Polygon polygon) {
        entrancePolygon = polygon;
    }

    public boolean isEntranceAccessible() {
        return isAccessible;
    }
}