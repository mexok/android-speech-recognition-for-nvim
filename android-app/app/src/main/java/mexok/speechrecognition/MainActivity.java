package mexok.speechrecognition;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.io.entity.StringEntity;

import java.io.IOException;
import java.util.ArrayList;


public class MainActivity extends AppCompatActivity {

    static final Integer RECORD_AUDIO_REQ_CODE = 6001;

    static final String SHARED_PREFERENCES_IP_KEY = "ip";
    static final String SHARED_PREFERENCES_PORT_KEY = "port";

    boolean isStarted = false;
    Button buttonRecording;
    EditText editTextIP, editTextPort;

    SpeechRecognizer speechRecognizer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        buttonRecording = findViewById(R.id.buttonRecording);
        buttonRecording.setOnClickListener(view -> toggleRecording());

        Button buttonTestConnection = findViewById(R.id.buttonTestConnection);
        buttonTestConnection.setOnClickListener(view -> testConnection());

        editTextIP = findViewById(R.id.editTextIP);
        editTextPort = findViewById(R.id.editTextPort);
        loadFromStorage();
        editTextIP.setOnEditorActionListener((textView, i, keyEvent) -> {
            saveToStorage();
            return false;
        });
        editTextPort.setOnEditorActionListener((textView, i, keyEvent) -> {
            saveToStorage();
            return false;
        });
        isStarted = false;
        setupSpeechRecognizer();
    }

    void loadFromStorage() {
        SharedPreferences sharedPreferences = getPreferences(MODE_PRIVATE);
        if (sharedPreferences.getString(SHARED_PREFERENCES_IP_KEY, null) != null) {
            editTextIP.setText(sharedPreferences.getString(SHARED_PREFERENCES_IP_KEY, null));
        }
        if (sharedPreferences.getString(SHARED_PREFERENCES_PORT_KEY, null) != null) {
            editTextPort.setText(sharedPreferences.getString(SHARED_PREFERENCES_PORT_KEY, null));
        }
    }

    void saveToStorage() {
        SharedPreferences sharedPreferences = getPreferences(MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(SHARED_PREFERENCES_IP_KEY, editTextIP.getText().toString());
        editor.putString(SHARED_PREFERENCES_PORT_KEY, editTextPort.getText().toString());
        editor.apply();
    }

    void setupSpeechRecognizer() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);

        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle bundle) {
            }

            @Override
            public void onBeginningOfSpeech() {
            }

            @Override
            public void onRmsChanged(float v) {
            }

            @Override
            public void onBufferReceived(byte[] bytes) {
            }

            @Override
            public void onEndOfSpeech() {
            }

            @Override
            public void onError(int i) {
                // Use a dirty hack for continuation of listening
                if (isStarted) {
                    stopSpeechRecognition();
                    startSpeechRecognition();
                }
            }

            @Override
            public void onResults(Bundle bundle) {
                ArrayList<String> results = bundle.getStringArrayList(
                        SpeechRecognizer.RESULTS_RECOGNITION
                );
                if (results.size() > 0) {
                    send(results.get(0));
                    Toast.makeText(MainActivity.this, results.get(0), Toast.LENGTH_SHORT).show();
                }

                // Use a dirty hack for continuation of listening
                if (isStarted) {
                    stopSpeechRecognition();
                    startSpeechRecognition();
                }
            }

            @Override
            public void onPartialResults(Bundle bundle) {
            }

            @Override
            public void onEvent(int i, Bundle bundle) {

            }
        });
    }

    void send(String words) {
        new Thread(() -> {
            try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
                HttpPost post = new HttpPost(getConnectionString() + "/send_voice_cmd");
                StringEntity json = new StringEntity(
                        "{\"results\":{\"words\":\"" + words + "\"}}",
                        ContentType.APPLICATION_JSON
                );
                post.setEntity(json);
                CloseableHttpResponse response = httpClient.execute(post);
                response.close();
            } catch (IOException | IllegalArgumentException e) {
                e.printStackTrace();
            }
        }).start();
    }

    String getConnectionString() {
        return "http://" + editTextIP.getText().toString() + ':' + editTextPort.getText().toString();
    }

    void testConnection() {
        new Thread(() -> {
            boolean wasSuccessful = false;
            try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
                HttpPost post = new HttpPost(getConnectionString() + "/connection_test");
                StringEntity json = new StringEntity("{}", ContentType.APPLICATION_JSON);
                post.setEntity(json);
                CloseableHttpResponse response = httpClient.execute(post);
                wasSuccessful = response.getCode() == 200;
                response.close();
            } catch (IOException | IllegalArgumentException e) {
                e.printStackTrace();
            }
            final String toastText = wasSuccessful ? "Connection successful!" : "Cannot connect!";
            runOnUiThread(() -> Toast.makeText(MainActivity.this, toastText, Toast.LENGTH_SHORT).show());
        }).start();
    }

    void toggleRecording() {
        if (!isStarted) {
            buttonRecording.setText(R.string.stop_recording);
            startSpeechRecognition();
        } else {
            buttonRecording.setText(R.string.start_recording);
            stopSpeechRecognition();
        }
        isStarted = !isStarted;
    }

    void startSpeechRecognition() {
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, RECORD_AUDIO_REQ_CODE);
            return;
        }

        Intent speechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE, true);
        speechRecognizer.startListening(speechRecognizerIntent);
    }

    void stopSpeechRecognition() {
        speechRecognizer.stopListening();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == RECORD_AUDIO_REQ_CODE && grantResults.length > 0 ) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startSpeechRecognition();
            }
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        speechRecognizer.destroy();
    }
}
