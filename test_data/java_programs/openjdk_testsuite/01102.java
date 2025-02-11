





import java.io.*;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;


public class CheckExamples {
    
    public static void main(String... args) throws Exception {
        boolean jtreg = (System.getProperty("test.src") != null);
        Path tmpDir;
        boolean deleteOnExit;
        if (jtreg) {
            
            tmpDir = Paths.get(System.getProperty("user.dir"));
            deleteOnExit = false;
        } else {
            tmpDir = Files.createTempDirectory(Paths.get(System.getProperty("java.io.tmpdir")),
                    CheckExamples.class.getName());
            deleteOnExit = true;
        }
        Example.setTempDir(tmpDir.toFile());

        try {
            new CheckExamples().run();
        } finally {
            if (deleteOnExit) {
                clean(tmpDir);
            }
        }
    }

    
    void run() throws Exception {
        Set<Example> examples = getExamples();

        Set<String> notYetList = getNotYetList();
        Set<String> declaredKeys = new TreeSet<String>();
        for (Example e: examples) {
            Set<String> e_decl = e.getDeclaredKeys();
            Set<String> e_actual = e.getActualKeys();
            for (String k: e_decl) {
                if (!e_actual.contains(k))
                    error("Example " + e + " declares key " + k + " but does not generate it");
            }
            for (String k: e_actual) {
                if (!e_decl.contains(k))
                    error("Example " + e + " generates key " + k + " but does not declare it");
            }
            for (String k: e.getDeclaredKeys()) {
                if (notYetList.contains(k))
                    error("Example " + e + " declares key " + k + " which is also on the \"not yet\" list");
                declaredKeys.add(k);
            }
        }

        ResourceBundle b =
            ResourceBundle.getBundle("com.sun.tools.javac.resources.compiler");
        Set<String> resourceKeys = new TreeSet<String>(b.keySet());

        for (String dk: declaredKeys) {
            if (!resourceKeys.contains(dk))
                error("Key " + dk + " is declared in tests but is not a valid key in resource bundle");
        }

        for (String nk: notYetList) {
            if (!resourceKeys.contains(nk))
                error("Key " + nk + " is declared in not-yet list but is not a valid key in resource bundle");
        }

        for (String rk: resourceKeys) {
            if (!declaredKeys.contains(rk) && !notYetList.contains(rk))
                error("Key " + rk + " is declared in resource bundle but is not in tests or not-yet list");
        }

        System.err.println(examples.size() + " examples checked");
        System.err.println(notYetList.size() + " keys on not-yet list");

        Counts declaredCounts = new Counts(declaredKeys);
        Counts resourceCounts = new Counts(resourceKeys);
        List<String> rows = new ArrayList<String>(Arrays.asList(Counts.prefixes));
        rows.add("other");
        rows.add("total");
        System.err.println();
        System.err.println(String.format("%-14s %15s %15s %4s",
                "prefix", "#keys in tests", "#keys in javac", "%"));
        for (String p: rows) {
            int d = declaredCounts.get(p);
            int r = resourceCounts.get(p);
            System.err.print(String.format("%-14s %15d %15d", p, d, r));
            if (r != 0)
                System.err.print(String.format(" %3d%%", (d * 100) / r));
            System.err.println();
        }

        if (errors > 0)
            throw new Exception(errors + " errors occurred.");
    }

    
    Set<Example> getExamples() {
        Set<Example> results = new TreeSet<Example>();
        File testSrc = new File(System.getProperty("test.src"));
        File examples = new File(testSrc, "examples");
        for (File f: examples.listFiles()) {
            if (isValidExample(f))
                results.add(new Example(f));
        }
        return results;
    }

    boolean isValidExample(File f) {
        return (f.isDirectory() && f.list().length > 0) ||
                (f.isFile() && f.getName().endsWith(".java"));
    }

    
    Set<String> getNotYetList() {
        Set<String> results = new TreeSet<String>();
        File testSrc = new File(System.getProperty("test.src"));
        File notYetList = new File(testSrc, "examples.not-yet.txt");
        try {
            String[] lines = read(notYetList).split("[\r\n]");
            for (String line: lines) {
                int hash = line.indexOf("#");
                if (hash != -1)
                    line = line.substring(0, hash).trim();
                if (line.matches("[A-Za-z0-9-_.]+"))
                    results.add(line);
            }
        } catch (IOException e) {
            throw new Error(e);
        }
        return results;
    }

    
    String read(File f) throws IOException {
        byte[] bytes = new byte[(int) f.length()];
        DataInputStream in = new DataInputStream(new FileInputStream(f));
        try {
            in.readFully(bytes);
        } finally {
            in.close();
        }
        return new String(bytes);
    }

    
    void error(String msg) {
        System.err.println("Error: " + msg);
        errors++;
    }

    int errors;

    
    static void clean(Path dir) throws IOException {
        Files.walkFileTree(dir, new SimpleFileVisitor<Path>() {
            @Override
            public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                Files.delete(file);
                return super.visitFile(file, attrs);
            }

            @Override
            public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
                if (exc == null) Files.delete(dir);
                return super.postVisitDirectory(dir, exc);
            }
        });
    }

    static class Counts {
        static String[] prefixes = {
            "compiler.err.",
            "compiler.warn.",
            "compiler.note.",
            "compiler.misc."
        };

        Counts(Set<String> keys) {
            nextKey:
            for (String k: keys) {
                for (String p: prefixes) {
                    if (k.startsWith(p)) {
                        inc(p);
                        continue nextKey;
                    }
                }
                inc("other");
            }
            table.put("total", keys.size());
        }

        int get(String p) {
             Integer i = table.get(p);
             return (i == null ? 0 : i);
        }

        void inc(String p) {
            Integer i = table.get(p);
            table.put(p, (i == null ? 1 : i + 1));
        }

        Map<String,Integer> table = new HashMap<String,Integer>();
    };
}
