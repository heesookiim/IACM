package com.example.iacm;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import androidx.fragment.app.FragmentActivity;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Polygon;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

import libs.mjn.prettydialog.PrettyDialog;
import libs.mjn.prettydialog.PrettyDialogCallback;


public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

        private GoogleMap mMap;


        void send_email() {
                Intent intent = new Intent(Intent.ACTION_SENDTO);
                intent.putExtra(Intent.EXTRA_EMAIL, "heyy");
                intent.putExtra(Intent.EXTRA_SUBJECT, "HEY");
                intent.putExtra(Intent.EXTRA_TEXT, "HEY");
                intent.setData(Uri.parse("mailto:"));
                if (intent.resolveActivity(getPackageManager()) != null) {
                        startActivity(intent);
                } else {
//                        Toast.makeText(Dialog.this,
//                                "There is no application that support this action",
//                                Toast.LENGTH_SHORT).show();
                }

        }


        void clickedBuilding(Building building, PrettyDialog dialog) {
                dialog.setTitle("Building Information");
                dialog.setMessage(building.getBuildingName());
                for (int i = 0; i <= building.getNumberOfFloors(); i++) {
                        int floor = i;
                        dialog.addButton(
                                "Floor " + i,
                                R.color.pdlg_color_white,
                                R.color.floor_button_color,
                                new PrettyDialogCallback() {
                                        @Override
                                        public void onClick() {
                                                building.setSelectedFloor(floor);
                                                dialog.dismiss();
                                        }
                                }
                        );
                }
                dialog.addButton(
                        "Report Issue",
                        R.color.pdlg_color_white,
                        R.color.report_issue_button_color,
                        new PrettyDialogCallback() {
                                @Override
                                public void onClick() {
                                        send_email();
                                        dialog.dismiss();
                                }
                        }
                );
                dialog.addButton(
                        "OK",                    // button text
                        R.color.pdlg_color_white,        // button text color
                        R.color.ok_button_color,        // button background color
                        new PrettyDialogCallback() {        // button OnClick listener
                                @Override
                                public void onClick() {
                                        dialog.dismiss();
                                }
                        }
                );
                dialog.show();
        }

        public void showLegend(View view) {
                //#FFEB3B
                //original yellow color of button
                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                // Get the layout inflater
                LayoutInflater inflater = this.getLayoutInflater();

                // Inflate and set the layout for the dialog
                // Pass null as the parent view because its going in the dialog layout
                builder.setView(inflater.inflate(R.layout.legend_dialog, null));

                AlertDialog legend_dialog = builder.create();
                legend_dialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();
                        }
                });
                legend_dialog.show();

                Button neutralButton = legend_dialog.getButton(AlertDialog.BUTTON_NEUTRAL);
                LinearLayout.LayoutParams neutralButtonLL = (LinearLayout.LayoutParams) neutralButton.getLayoutParams();
                neutralButton.setTextSize(20);
                neutralButtonLL.gravity = Gravity.CENTER;
                neutralButtonLL.weight = 10;
                neutralButton.setLayoutParams(neutralButtonLL);
        }


        @Override
        protected void onCreate(Bundle savedInstanceState) {
                super.onCreate(savedInstanceState);
                setContentView(R.layout.activity_maps);
                // Obtain the SupportMapFragment and get notified when the map is ready to be used.
                SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                        .findFragmentById(R.id.map);
                mapFragment.getMapAsync(this);
        }


        LatLng addCoordinate(String coordinate) {
                String [] temp = coordinate.split(", ");
                String x = temp[0].trim().substring(1).trim();
                double xCoord = Double.parseDouble(x);
                String y = temp[1].trim().substring(0, temp[1].trim().length() - 1).trim();
                double yCoord = Double.parseDouble(y);
                LatLng newCoord = new LatLng(xCoord, yCoord);
                return newCoord;
        }


        Building addBuilding(List <String> inputData, String buildingCode, String buildingName, int start, int end) {
                //Read building's coordinates
                int buildingCoordEnd = 0;
                ArrayList <LatLng> buildingCoords = new ArrayList<>();
                for(int i = start; i < inputData.size(); i++) {
                        if(inputData.get(i).charAt(0) != '(') {
                                //No more building coordinates
                                buildingCoordEnd = i;
                                break;
                        } else {
                                //Add building coordinates
                                buildingCoords.add(addCoordinate(inputData.get(i)));
                        }
                }
                //Add Building object
                Building newBuilding = new Building(buildingName, buildingCode, buildingCoords);
                Polygon newPolygon = mMap.addPolygon(newBuilding.getBuildingPolygonOptions());
                newBuilding.setBuildingPolygon(newPolygon);
                newPolygon.setClickable(true);

                //If there's no defined components for the given building
                if(inputData.get(buildingCoordEnd+1).equals("Building")) {
                        return newBuilding;
                }

                //Read Entrances and Bathrooms
                for(int i = buildingCoordEnd; i < end; i++) {
                        //Create Entrance
                        if(inputData.get(i).equals("Entrance")) {
                                int ent = i + 1; //entrance code line
                                String entranceCode = inputData.get(ent);
                                ent++;
                                ArrayList<LatLng> entranceCoords = new ArrayList<>();
                                boolean isAccessible = false;
                                while (!inputData.get(ent).equals("Entrance") || !inputData.get(ent).equals("Bathroom")) {
                                        if (inputData.get(ent).charAt(0) == '(') {
                                                //Add entrance coordinate
                                                entranceCoords.add(addCoordinate(inputData.get(ent)));
                                        }
                                        if (inputData.get(ent).equals("True")) {
                                                //Entrance is accessible
                                                ent++;
                                                isAccessible = true;
                                                break;
                                        }
                                        if (inputData.get(ent).equals("False")) {
                                                //Entrance is not accessible
                                                ent++;
                                                break;
                                        }
                                        ent++;
                                }
                                //Add entrance polygon/info
                                Entrance newEntrance = new Entrance(entranceCode, entranceCoords, isAccessible);
                                newBuilding.addEntrance(newEntrance);
                                newEntrance.setEntrancePolygon(mMap.addPolygon(newEntrance.getEntrancePolygonOptions()));
                                i = ent;
                        }

                        //Create Bathroom
                        if(inputData.get(i).equals("Bathroom")) {
                                int bath = i+1;
                                String bathroomCode = inputData.get(bath);
                                bath++;
                                ArrayList <LatLng> bathroomCoords = new ArrayList<>();
                                boolean bathroomAccessible = false;
                                Integer level = 0;
                                while(!inputData.get(bath).equals("Building") || i == inputData.size() || !inputData.get(bath).equals("Bathroom")) {
                                        if(inputData.get(bath).charAt(0) == '(') {
                                                //Add bathroom coordinate
                                                bathroomCoords.add(addCoordinate(inputData.get(bath)));
                                        }
                                        if(Character.isDigit(inputData.get(bath).charAt(0))) {
                                                //Add bathroom floor level
                                                level = Character.getNumericValue(inputData.get(bath).charAt(0));
                                        }
                                        if(inputData.get(bath).equals("True")) {
                                                //Bathroom is accessible
                                                bathroomAccessible = true;
                                                bath++;
                                                break;
                                        }
                                        if(inputData.get(bath).equals("False")) {
                                                //Bathroom is not accessible
                                                bath++;
                                                break;
                                        }
                                        bath++;
                                }
                                //Add bathroom polygon/info
                                Bathroom newBathroom = new Bathroom(bathroomCode, level, buildingCode, bathroomCoords, bathroomAccessible);
                                newBuilding.addBathroom(newBathroom);
                                newBathroom.setBathroomPolygon(mMap.addPolygon(newBathroom.getBathroomPolygonOptions()));
                                i = bath;
                        }
                        if(inputData.get(i).equals("Building") || inputData.get(i).equals("Finished")) {
                                newBuilding.setFloorToZero();
                                return newBuilding;
                        }
                        i--;
                }
                newBuilding.setFloorToZero();
                return newBuilding;
        }


        List <Building> createBuildingList(List<String> inputData, List<Integer> buildingLines) {
                List <Building> buildings = new ArrayList<>();
                int line = 0;
                for(int ind = 0; ind < buildingLines.size(); ind++) {
                        int i = buildingLines.get(ind);
                        //Add building to map
                        String buildingCode = inputData.get(i+1).toUpperCase();
                        System.out.println(buildingCode);

                        //Add building name
                        String buildingName = inputData.get(i+2);
                        System.out.println(buildingName);

                        //Create Building polygon
                        Building newBuilding;
                        if(line == buildingLines.size()-1) { //Last building
                                newBuilding = addBuilding(inputData, buildingCode, buildingName, i+3, inputData.size());
                                buildings.add(newBuilding);
                                return buildings;
                        } else {
                                line++;
                        }
                        //Add building elements
                        newBuilding = addBuilding(inputData, buildingCode, buildingName, i+3, buildingLines.get(line));
                        buildings.add(newBuilding);
                }
                return buildings;
        }


        protected List<String> readTextFromURL(String urlString) {
                URLConnection feedUrl;
                List<String> placeAddress = new ArrayList<>();
                try {
                        feedUrl = new URL(urlString).openConnection();
                        InputStream is = feedUrl.getInputStream();
                        BufferedReader reader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
                        String line;
                        while ((line = reader.readLine()) != null) {
                                placeAddress.add(line); //add line to list
                        }
                        is.close(); //close input stream
                        return placeAddress; //return whatever you need
                }
                catch (Exception e) {
                        e.printStackTrace();
                }
                return null;
        }


        List <Building> readBuildingData() {
                StrictMode.ThreadPolicy gfgPolicy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
                StrictMode.setThreadPolicy(gfgPolicy);

                //Get building data from server as String data
                List <String> lines = readTextFromURL("https://epics.ecn.purdue.edu/mobi/BuildingData.txt");

                //Indexes where building gets declared
                List <Integer> buildingIndexes = new ArrayList<>();
                for(int i = 0; i < lines.size(); i++) {
                        if (lines.get(i).equals("Building")) {
                                buildingIndexes.add(i);
                        }
                }
                List <Building> buildingList = createBuildingList(lines, buildingIndexes);

                return buildingList;
        }


        /**
         * Manipulates the map once available.
         * This callback is triggered when the map is ready to be used.
         * This is where we can add markers or lines, add listeners or move the camera. In this case,
         * we just add a marker near Sydney, Australia.
         * If Google Play services is not installed on the device, the user will be prompted to install
         * it inside the SupportMapFragment. This method will only be triggered once the user has
         * installed Google Play services and returned to the app.
         */
        @Override
        public void onMapReady(GoogleMap googleMap) {
                mMap = googleMap;
                long startTime = System.nanoTime(); //Start stopwatch for performance evaluation
                List <Building> purdueCampus = new ArrayList<>(); //List of Buildings on campus
                try {
                        purdueCampus = readBuildingData();
                } catch (Exception e) {
                        e.printStackTrace();
                }

                LatLng PurdueArch = new LatLng(40.431625, -86.916490);
                mMap.moveCamera(CameraUpdateFactory.newLatLng(PurdueArch));
                mMap.setMinZoomPreference(14);
                List<Building> finalPurdueCampus = purdueCampus;

                long endTime = System.nanoTime(); //End stopwatch for performance evaluation
                long duration = endTime - startTime;
                System.out.println("Runtime = " + duration/1000000 + " ms");

                mMap.setOnPolygonClickListener(new GoogleMap.OnPolygonClickListener() {
                        public void onPolygonClick(Polygon polygon) {
                                PrettyDialog dialog = new PrettyDialog(MapsActivity.this)
                                        .setIcon(R.drawable.baseline_apartment_purple_500_48dp);
                                int buildings = finalPurdueCampus.size();

                                for(int j = 0; j < buildings; j++) {
                                        if(polygon.equals(finalPurdueCampus.get(j).getBuildingPolygon())) {
                                                clickedBuilding(finalPurdueCampus.get(j), dialog);
                                        }
                                }
                                Log.d("LOG", "Dialog made");
                        }
                });
        }
}
