using System.Text;
using System.Text.Json;

class Program
{
    private const string Url = "http://127.0.0.1:5000/get-command";

    static async Task Main(string[] args)
    {
        Console.WriteLine("Tell me what concentrate sample to make (Q or q to quit) ");
        while (true)
        {
            var request = Console.ReadLine();

             if (request is "Q" or "q")
                 return;
            
             
             Console.WriteLine("Processing request ....");
            
            using var client = new HttpClient();

            // Prepare the JSON payload
            var payload = new { request };
            var jsonPayload = JsonSerializer.Serialize(payload);

            // Call the tokenizer API
            var response = await client.PostAsync(
                Url,
                new StringContent(jsonPayload, Encoding.UTF8, "application/json")
            );

            // Parse the response
            var result = await response.Content.ReadAsStringAsync();
            Console.WriteLine("Response: " + result);
        }
    }
}