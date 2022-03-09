# coding: utf8

import os, clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("IronPython.Wpf")
import wpf
from System.Windows import Application
from System.Windows.Markup import XamlReader
 
xaml = """<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xml:lang="ja-JP"
    Width = "508.48" Height="500" Background="#FFF1F1F1">
    <StackPanel>
        <StatusBar Height="35" Background="#FF6898C9">
            <Button Content="Upload" Width="100" Margin="15,0,0,0" Background="#FFFFBE70"/>
            <Button Content="Options" Width="100" Background="#FFD5EAFF"/>
            <Button Content="Cancel" Width="100" Margin="150,0,0,0" Background="#FFD5EAFF"/>
        </StatusBar>
        <StackPanel Margin="20" Orientation="Horizontal" Height="399">
            <ScrollViewer Width="215">
                <StackPanel Margin="5">
                    <Label Content="Issue" Height="40" FontSize="22" FontWeight="Bold"/>
                    <Label Content="Created by : ZOE" Height="30" FontSize="14"/>
                    <Label Content="Assigned to :" Height="30" FontSize="14"/>
                    <ComboBox Margin="3" Height="22">
                        <ComboBoxItem Content="ぞえぞえ"/>
                    </ComboBox>
                    <Label Content="Title :" Height="30" FontSize="14"/>
                    <TextBox TextWrapping="Wrap" Height="24" Margin="3" Text="リビングの内壁仕上"/>
                    <Label Content="Details :" Height="30" FontSize="14"/>
                    <TextBox TextWrapping="Wrap" Height="73" Margin="3" Text="一階リビングの内壁は、下地材を貼るか直接塗装するかどちらが良いでしょうか？"/>
                    <Label Content="Due Data :" Height="30" FontSize="14"/>
                    <Calendar OverridesDefaultStyle="True"/>
                </StackPanel>
            </ScrollViewer>
            <ScrollViewer Margin="20,0,0,0" Width="215">
                <StackPanel >
                    <Label Content="Family Data" Height="40" FontSize="22" FontWeight="Bold"/>
                    <Label Content="Category : Basic" Height="30" FontSize="14"/>
                    <Label Content="Type : StoneMassony" Height="30" FontSize="14"/>
                    <Label Content="ID : 493648" Height="30" FontSize="14"/>
                    <Label Content="Parameters :" Height="30" FontSize="14"/>
                    <TreeView FontSize="12" Margin="3" Background="White">
                        <TreeViewItem Header="拘束">
                            <TreeViewItem Header="配置基準 (ElementID)"/>
                            <TreeViewItem Header="基準レベル (ElementID)"/>
                            <TreeViewItem Header="基準レベル オフセット (float)"/>
                            <TreeViewItem Header="上部レベル (ElementID)"/>
                            <TreeViewItem Header="上部レベル オフセット (float)"/>
                            <TreeViewItem Header="部屋境界 (bool)"/>
                        </TreeViewItem>
                        <TreeViewItem Header="断面定義">
                            <TreeViewItem Header="断面 (String)"/>
                        </TreeViewItem>
                        <TreeViewItem Header="構造">
                            <TreeViewItem Header="構造 (bool)"/>
                        </TreeViewItem>
                        <TreeViewItem Header="識別情報">
                            <TreeViewItem Header="イメージ (String)"/>
                            <TreeViewItem Header="コメント (String)"/>
                            <TreeViewItem Header="マーク (String)"/>
                        </TreeViewItem>
                        <TreeViewItem Header="フェーズ">
                            <TreeViewItem Header="構築フェーズ (ElementID)"/>
                            <TreeViewItem Header="解体フェーズ (ElementID)"/>
                        </TreeViewItem>
                    </TreeView>
                </StackPanel>
            </ScrollViewer>
        </StackPanel>
    </StackPanel>
</Window>"""
 
w = XamlReader.Parse(xaml)
Application().Run(w)