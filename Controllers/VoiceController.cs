using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using VoiceDetectionAPI.Models;

[ApiController]
[Route("api/voice-detection")]
public class VoiceController : ControllerBase
{
    private const string API_KEY = "test123";
    private readonly PythonService _python;

    public VoiceController(PythonService python)
    {
        _python = python;
    }

    [HttpPost]
    public IActionResult Detect(
    [FromHeader(Name = "x-api-key")] string apiKey,
    [FromBody] VoiceRequest request)
    {
        if (apiKey != "test123")
            return Unauthorized(new { status = "error", message = "Invalid API key or malformed request" });

        JsonElement result = _python.Analyze(request.audioBase64);

        string classification = result.GetProperty("classification").GetString();
        double confidence = result.GetProperty("confidenceScore").GetDouble();
        string explanation = result.GetProperty("explanation").GetString();

        return Ok(new
        {
            status = "success",
            language = request.language,
            classification = classification,
            confidenceScore = confidence,
            explanation = explanation
        });
    }

}
