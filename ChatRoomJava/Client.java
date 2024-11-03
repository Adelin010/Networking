import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client implements Runnable{
    
    private Socket client;
    private BufferedReader in;
    private PrintWriter out;
    private boolean done;


    @Override
    public void run(){
        try {
            client = new Socket("127.0.0.1", 9898);
            out = new PrintWriter(client.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(client.getInputStream()));

            InHandler inHandler = new InHandler();
            Thread t = new Thread(inHandler);
            t.start();

            String inMess;
            while((inMess = in.readLine()) != null){
                System.out.println(inMess);
            }
        } catch (IOException e) {
            shutdown();
        }
    }


    public void shutdown(){
        done = true;
        try{
            in.close();
            out.close();
            if(!client.isClosed())
                client.close();
            
        }catch(Exception exp){
            exp.printStackTrace();
        }
    }

    class InHandler implements Runnable{

        @Override 
        public void run(){
            try {
                BufferedReader inReader = new BufferedReader(new InputStreamReader(System.in));
                while(!done){
                    String message = inReader.readLine();
                    if(message.equals("/quit")){
                        out.println("/quit");
                        inReader.close();
                        shutdown();
                    }else{
                        out.println(message);
                    }
                }
            } catch (Exception e) {
                shutdown();
            }
        }
    }

    public static void main(String[] args) {
        Client client = new Client();
        client.run();
    }
}
