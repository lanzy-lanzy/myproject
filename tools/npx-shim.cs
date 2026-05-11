using System;
using System.Diagnostics;
using System.IO;

class NpxShim
{
    static int Main(string[] args)
    {
        var npxCmd = FindOnPath("npx.cmd");
        if (npxCmd == null)
        {
            Console.Error.WriteLine("npx.cmd was not found on PATH. Install Node.js and npm, then retry.");
            return 1;
        }

        var command = "\"\"" + npxCmd + "\" " + string.Join(" ", Array.ConvertAll(args, QuoteForCmd)) + "\"";
        var startInfo = new ProcessStartInfo
        {
            FileName = "cmd.exe",
            Arguments = "/D /C " + command,
            UseShellExecute = false,
        };

        using (var process = Process.Start(startInfo))
        {
            process.WaitForExit();
            return process.ExitCode;
        }
    }

    static string FindOnPath(string fileName)
    {
        var path = Environment.GetEnvironmentVariable("PATH") ?? "";
        foreach (var rawDir in path.Split(Path.PathSeparator))
        {
            if (string.IsNullOrWhiteSpace(rawDir))
            {
                continue;
            }

            var dir = rawDir.Trim('"');
            var candidate = Path.Combine(dir, fileName);
            if (File.Exists(candidate))
            {
                return candidate;
            }
        }

        return null;
    }

    static string QuoteForCmd(string value)
    {
        return "\"" + value.Replace("\"", "\\\"") + "\"";
    }
}
