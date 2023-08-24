package net.synqg.qg.service;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;

import org.json.JSONException;
import org.json.JSONObject;

import static net.synqg.qg.utils.SynQgUtils.*;

class Pair<T, U> {
    public final T first;
    public final U second;

    public Pair(T first, U second) {
        this.first = first;
        this.second = second;
    }

    public T getKey() {
        return first;
    }

    public U getValue() {
        return second;
    }
}

/**
 * Service which generates questions from the
 *
 * @author kaustubhdholé.
 */
public class QuestionGenerationConsoleService {

    private static SynQGService questionGenerator;
    private static boolean printLogs = false;

    static String progressBar(int progressBarSize, long currentPosition, long startPositoin, long finishPosition) {
        String bar = "";
        int nPositions = progressBarSize;
        char pb = '░';
        char stat = '█';
        for (int p = 0; p < nPositions; p++) {
            bar += pb;
        }
        int ststus = (int) (100 * (currentPosition - startPositoin) / (finishPosition - startPositoin));
        int move = (nPositions * ststus) / 100;
        return "[" + bar.substring(0, move).replace(pb, stat) + ststus + "%" + bar.substring(move, bar.length()) + "]" + currentPosition + "/" + finishPosition;
    }

    // read file to lines
    public static List<JSONObject> readJsonLinesToObjects(String filePath) {
        List<String> lines = new ArrayList<>();
        List<JSONObject> out = new ArrayList<>();
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "UTF-8"));
            String line;
            while ((line = br.readLine()) != null) {
                lines.add(line.trim());
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // parse json
        for (int i = 0; i < lines.size(); i++) {
            try {
                JSONObject jsonObject = new JSONObject(lines.get(i));
                out.add(jsonObject);
            } catch (JSONException e) {
                System.out.println(lines.get(i));
                e.printStackTrace();
            }
        }
        return out;
    }

    // clean comments
    public static String cleanComment(String comment) {
        // remove string contiguous spaces
        comment = comment.replace("@&", ",").replaceAll("\\s+", " ");
        // remove comment start and end
        comment = comment.replace("/*", "").replace("*/", "");
        // remove inline comment start
        comment = comment.replace("//", "");
        return comment;
    }

    public static void run() throws IOException {
        questionGenerator = new SynQGService(true, true, false, printLogs);
        System.out.println("Ensure that you have the NLP server and the back-translation server on.");

        String inputFileName = "/data/wangjun/CodeQG/data/all_data/Inline600-800_clean_half1.jsonl";
        String outputFileName = "/data/wangjun/CodeQG/data/all_data/Output600-800_clean_half1.jsonl";
        
        List<JSONObject> lines = readJsonLinesToObjects(inputFileName);
        // create empty contents with lines length
        List<JSONObject> contents = new ArrayList<>();
        for (int i = 0; i < lines.size(); i++) {
            contents.add(null);
        }
        // int failedCount = 0;
        List<Integer> counter = new ArrayList<>();

        // string list with id
        List<Pair<Integer, JSONObject>> inputs = new ArrayList<>();

        for (int i = 0; i < lines.size(); i++) {
            inputs.add(new Pair<Integer, JSONObject>(i, lines.get(i)));
        }

        // if outfile exits, count line number
        int lineCount = 0;
        if (new File(outputFileName).exists()) {
            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(outputFileName), "UTF-8"));
            String line;
            while ((line = br.readLine()) != null) {
                JSONObject jsonObject = new JSONObject(line.trim());
                contents.set(lineCount, jsonObject);
                lineCount++;
            }
            br.close();
        }

        if (lineCount != 0) {
            System.out.println("Loaded " + lineCount + "lines from output file.");
        }

        for (int i = 0; i < inputs.size(); ++i) {
            // 断点继续功能
            if (i < lineCount) {
                counter.add(i);
                continue;
            }
            single_line_parse(inputs.get(i), contents, counter);
            System.out.println(progressBar(100, counter.size(), 0, lines.size()));
            if (i % 100 == 0) {
                write(outputFileName, contents);
            }
        }
        

        write(outputFileName, contents);
        // System.out.println("how many failed" + failedCount);
    }

    public static void main(String[] args) throws IOException {
        run();
        System.exit(0);
    }

    public static void write(String fileName, List<JSONObject> contents) throws IOException {
        String tmpFilePath = fileName + ".temp";
        System.out.println("写文件");
        // write to utf8
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(tmpFilePath), "UTF-8"));
        for (JSONObject cont : contents) {
            if (cont == null) {
                break;
            }
            bw.write(cont.toString() + "\n");
        }
        bw.close();

        // delete old file
        File oldFile = new File(fileName);
        if(!oldFile.delete()){
            System.out.println("旧文件删除失败！");
        }

        // copy file tmpFilePath to fileName
        File newFile = new File(tmpFilePath);
        if(!newFile.renameTo(oldFile)){
            System.out.println("文件重命名失败！");
        }
    }

    public static void single_line_parse(Pair<Integer, JSONObject> pair, List<JSONObject> contents, List<Integer> counter) {
        int i = pair.getKey();
        JSONObject strLine = pair.getValue();

        if (strLine == null )
        {
            counter.add(i);
            return;
        }
        List<JSONObject> qaList = new ArrayList<>();
        String commentRaw = strLine.getString("inline_comment");
        String comment = cleanComment(commentRaw);

        if (comment.length() > 4096) {
            // 注释太长了，里面注释的可能是代码
            contents.set(i, strLine);
            // failedCount ++;
            counter.add(i);
            return;
        }

        try {
            questionGenerator.generateQuestionAnswers(comment)
                .forEach(q -> {
                    JSONObject qa = new JSONObject();
                    qa.put("question", q.question());
                    qa.put("answer", q.shortAnswer());
                    qaList.add(qa);
                });
            strLine.put("qa", qaList);
            contents.set(i, strLine);
        } catch(Exception e) {
            System.out.println("这句话有错误：" + comment);
            contents.set(i, strLine);
            // failedCount ++;
            counter.add(i);
            return;
        }
        counter.add(i);
    }
}
