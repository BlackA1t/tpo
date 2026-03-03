package com.example.linear.layout.notes;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private static final String STATE_NOTES = "state_notes";

    private EditText nEdit;
    private ArrayList<String> notes;
    private ArrayAdapter<String> adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        nEdit = findViewById(R.id.note_edit);
        ListView nList = findViewById(R.id.note_list);
        Button buttonAdd = findViewById(R.id.button_add);

        notes = new ArrayList<>();
        adapter = new ArrayAdapter<>(
                this,
                android.R.layout.simple_list_item_1,
                notes
        );
        nList.setAdapter(adapter);

        if (savedInstanceState != null) {
            ArrayList<String> saved = savedInstanceState.getStringArrayList(STATE_NOTES);
            if (saved != null) {
                notes.addAll(saved);
                adapter.notifyDataSetChanged();
            }
        }

        buttonAdd.setOnClickListener(this);
        nList.setOnItemClickListener((parent, view, position, id) -> {
            notes.remove(position);
            adapter.notifyDataSetChanged();
        });
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.button_add) {
            String text = nEdit.getText().toString().trim();

            if (!text.isEmpty()) {
                notes.add(0, text);
                adapter.notifyDataSetChanged();
                nEdit.setText("");
            }
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putStringArrayList(STATE_NOTES, notes);
    }
}