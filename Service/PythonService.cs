using System.Diagnostics;
using System.Text.Json;

public class PythonService
{
    public JsonElement Analyze(string base64Audio)
    {
        var psi = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = "predict.py",
            WorkingDirectory = Path.Combine(
                Directory.GetCurrentDirectory(), "python_ai"
            ),
            RedirectStandardInput = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using var process = Process.Start(psi);

        process.StandardInput.Write(base64Audio);
        process.StandardInput.Close();

        string output = process.StandardOutput.ReadToEnd();
        string error = process.StandardError.ReadToEnd();

        process.WaitForExit();

        if (!string.IsNullOrWhiteSpace(error))
            throw new Exception("Python error: " + error);

        return JsonSerializer.Deserialize<JsonElement>(output);
    }
}
