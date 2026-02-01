namespace VoiceDetectionAPI.Models;

public class VoiceRequest
{
    public string language { get; set; }
    public string audioFormat { get; set; }
    public string audioBase64 { get; set; }
}
