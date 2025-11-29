package com.arielgos.mcpfa

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ListView
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST
import java.text.SimpleDateFormat
import java.time.Instant
import java.util.Date


const val url = "https://7086215096ce.ngrok-free.app"


enum class MessageType {
    USER, SYSTEM
}

data class Chat(val message: String)

interface LMService {
    @POST("chat") fun postChat(@Body chat: Chat?): Call<Chat?>?
}

data class Message(val message: String, val type: MessageType)


class MainActivity : AppCompatActivity() {

    private val messages: MutableList<Message> = mutableListOf()

    private var list: ListView? = null

    private var txtMessage: EditText? = null
    private var btnSend: Button? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        val adapter: MessageAdapter = MessageAdapter(this@MainActivity, messages)
        list = findViewById(R.id.list)
        list?.setAdapter(adapter);

        txtMessage = findViewById(R.id.message)
        btnSend = findViewById(R.id.send)

        btnSend?.setOnClickListener(View.OnClickListener {
            val userMessage = txtMessage?.text.toString()
            if (userMessage.isBlank()) return@OnClickListener

            messages.add(Message(userMessage, MessageType.USER))
            txtMessage?.setText("")
            adapter.notifyDataSetChanged()


            val retrofit = Retrofit.Builder().baseUrl(url).addConverterFactory(GsonConverterFactory.create()).build()

            val apiService: LMService = retrofit.create(LMService::class.java)

            val call: Call<Chat?>? = apiService.postChat(Chat(message = userMessage)) // Can be null
            call?.enqueue(object : retrofit2.Callback<Chat?> {
                override fun onResponse(call: Call<Chat?>, response: Response<Chat?>) {
                    if (response.isSuccessful) {
                        response.body()?.let {
                            messages.add(Message(it.message, MessageType.SYSTEM))
                            adapter.notifyDataSetChanged()
                        }
                    }
                }

                override fun onFailure(call: Call<Chat?>, t: Throwable) { // Handle network or other errors, e.g., show a message to the user
                    messages.add(Message("Error: ${t.message}", MessageType.SYSTEM))
                    adapter.notifyDataSetChanged()
                }
            })

        })
    }

    class MessageAdapter(context: Context, messages: MutableList<Message>) : ArrayAdapter<Message?>(context, 0, messages) {
        override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
            val message: Message? = getItem(position)
            var convertView = LayoutInflater.from(getContext()).inflate(R.layout.message_item, parent, false)
            if (message?.type == MessageType.SYSTEM) {
                convertView = LayoutInflater.from(getContext()).inflate(R.layout.system_message_item, parent, false)
            }
            val tvMessage = convertView.findViewById<View?>(R.id.message) as TextView
            val tvDate = convertView.findViewById<View?>(R.id.date) as TextView
            tvMessage.setText(message?.message)
            tvDate.setText(SimpleDateFormat("dd/MM/yyyy HH:mm").format(Date.from(Instant.now())))
            return convertView
        }
    }

}